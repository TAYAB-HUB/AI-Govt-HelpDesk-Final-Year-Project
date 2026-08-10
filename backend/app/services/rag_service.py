"""
RAG (Retrieval-Augmented Generation) Service
Handles document ingestion, embedding, retrieval, and LLM generation
"""
import os
import httpx
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings as ChromaSettings
from pypdf import PdfReader
import pdfplumber
from pathlib import Path

from app.core.config import settings

class RAGService:
    def __init__(self):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        # Initialize ChromaDB with persistence
        os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        
        # Ollama client configuration
        self.ollama_base_url = settings.OLLAMA_BASE_URL
        self.ollama_model = settings.OLLAMA_MODEL
        self.ollama_available = self._check_ollama_availability()
    
    def _check_ollama_availability(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = httpx.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            print("⚠️  Ollama not available - using fallback mode")
            return False
    
    def get_or_create_collection(self, department_id: int):
        """Get or create a ChromaDB collection for a department."""
        collection_name = f"dept_{department_id}_docs"
        try:
            collection = self.chroma_client.get_collection(collection_name)
        except:
            collection = self.chroma_client.create_collection(
                name=collection_name,
                metadata={"department_id": department_id}
            )
        return collection
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed: {e}, trying pypdf...")
            with open(file_path, 'rb') as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        return text
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """Split text into overlapping chunks."""
        chunk_size = chunk_size or settings.CHUNK_SIZE
        overlap = overlap or settings.CHUNK_OVERLAP
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to end at a sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                boundary = max(last_period, last_newline)
                if boundary > chunk_size // 2:
                    chunk = chunk[:boundary + 1]
                    end = start + len(chunk)
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if len(c) > 50]  # Filter very small chunks
    
    def ingest_document(
        self, 
        document_id: int,
        department_id: int,
        file_path: str,
        title: str,
        file_type: str
    ) -> int:
        """
        Ingest a document into the vector store.
        Returns the number of chunks created.
        """
        # Extract text based on file type
        if file_type.lower() == 'pdf':
            text = self.extract_text_from_pdf(file_path)
        else:  # txt or other text formats
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        
        # Chunk the text
        chunks = self.chunk_text(text)
        
        # Get collection for this department
        collection = self.get_or_create_collection(department_id)
        
        # Generate embeddings and store
        embeddings = self.embedding_model.encode(chunks).tolist()
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_id = f"doc_{document_id}_chunk_{i}"
            
            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "document_id": document_id,
                    "document_title": title,
                    "chunk_index": i,
                    "department_id": department_id
                }]
            )
        
        return len(chunks)
    
    def retrieve_relevant_chunks(
        self,
        question: str,
        department_id: int,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant document chunks for a question.
        """
        top_k = top_k or settings.MAX_RETRIEVED_CHUNKS
        
        collection = self.get_or_create_collection(department_id)
        
        # Calculate question embedding
        query_embedding = self.embedding_model.encode([question]).tolist()
        
        # Query the collection
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        
        # Format results
        chunks = []
        if results['ids'] and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                chunks.append({
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i] if 'distances' in results else None
                })
        
        return chunks
    
    async def generate_answer_ollama(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]]
    ) -> str:
        """
        Generate an answer using Ollama LLM.
        """
        if not self.ollama_available:
            return self._generate_fallback_answer(context_chunks)
        
        # Build context from chunks
        context = "\n\n".join([
            f"[From: {chunk['metadata']['document_title']}]\n{chunk['text']}"
            for chunk in context_chunks
        ])
        
        # Create prompt
        prompt = f"""You are a helpful government employee helpdesk assistant. Answer the question based ONLY on the provided context. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {question}

Answer (be concise and cite the source document):"""
        
        try:
            async with httpx.AsyncClient(timeout=settings.OLLAMA_TIMEOUT) as client:
                response = await client.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.ollama_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "top_p": 0.9,
                            "max_tokens": 300
                        }
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "").strip()
                else:
                    print(f"Ollama error: {response.status_code}")
                    return self._generate_fallback_answer(context_chunks)
        
        except Exception as e:
            print(f"Ollama generation failed: {e}")
            return self._generate_fallback_answer(context_chunks)
    
    def _generate_fallback_answer(self, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate a template-based answer when Ollama is unavailable.
        """
        if not context_chunks:
            return "I don't have enough information to answer this question."
        
        # Simple extractive answer: return the most relevant chunk
        best_chunk = context_chunks[0]
        doc_title = best_chunk['metadata']['document_title']
        
        return f"Based on the document '{doc_title}', here is the relevant information:\n\n{best_chunk['text'][:300]}..."
    
    def calculate_confidence(self, chunks: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score based on retrieval distances.
        Lower distance = higher confidence.
        """
        if not chunks or chunks[0].get('distance') is None:
            return 0.5  # Default medium confidence
        
        # Convert distance to confidence (distance is typically 0-2)
        min_distance = chunks[0]['distance']
        confidence = max(0, min(1, 1 - (min_distance / 2)))
        return round(confidence, 2)
    
    def delete_document_from_index(self, document_id: int, department_id: int):
        """Remove all chunks of a document from the vector store."""
        collection = self.get_or_create_collection(department_id)
        
        # Get all chunk IDs for this document
        results = collection.get(
            where={"document_id": document_id}
        )
        
        if results['ids']:
            collection.delete(ids=results['ids'])

# Global instance
rag_service = RAGService()