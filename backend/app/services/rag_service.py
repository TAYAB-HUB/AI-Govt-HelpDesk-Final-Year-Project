"""
RAG pipeline module.

Flow:
  1. chunk_text()            -> split raw document text into overlapping chunks
  2. get_embedder()          -> lazily load sentence-transformers model (singleton)
  3. get_chroma_collection() -> one persistent Chroma collection per department
  4. ingest_document()       -> embed chunks + store in Chroma with metadata
  5. retrieve()               -> embed the question, similarity-search Chroma
  6. generate_answer()        -> call local Ollama with retrieved context;
                                 falls back to a template answer if Ollama is
                                 unreachable/errors, so the demo never crashes.

ASSUMPTION: similarity score is derived from Chroma's L2 distance,
normalized to a 0..1 "confidence" where 1.0 = perfect match. The exact
formula is an implementation choice, not specified in the project plan.
"""
import os
import re
import logging
from functools import lru_cache
from typing import List, Tuple

import chromadb
import httpx

from app.core.config import settings

logger = logging.getLogger("rag")


def extract_text(file_path: str, filename: str) -> str:
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if ext == "pdf":
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    chunk_size = chunk_size or settings.CHUNK_SIZE_CHARS
    overlap = overlap or settings.CHUNK_OVERLAP_CHARS
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks


class _FallbackEmbedder:
    """
    Deterministic bag-of-words hashing embedder used ONLY if the real
    sentence-transformers model cannot be loaded (e.g. no internet access to
    download weights on first run). Keeps the system demoable end-to-end
    instead of crashing, matching the plan's "graceful fallback" philosophy.
    Not semantically strong -- swap for the real model whenever possible.
    """
    DIM = 384

    def encode(self, texts: List[str], **kwargs) -> List[List[float]]:
        import hashlib
        import math
        vectors = []
        for t in texts:
            vec = [0.0] * self.DIM
            for word in re.findall(r"[a-z0-9]+", t.lower()):
                h = int(hashlib.md5(word.encode()).hexdigest(), 16)
                idx = h % self.DIM
                vec[idx] += 1.0
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            vectors.append([v / norm for v in vec])
        return vectors


@lru_cache(maxsize=1)
def get_embedder():
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        logger.info("Loaded sentence-transformers model: %s", settings.EMBEDDING_MODEL_NAME)
        return model
    except Exception as e:  # pragma: no cover - environment dependent
        logger.warning(
            "Could not load sentence-transformers model (%s). Falling back to "
            "lightweight hashing embedder. RAG relevance will be degraded until "
            "this is fixed (usually a missing internet connection on first run).", e,
        )
        return _FallbackEmbedder()


def embed(texts: List[str]) -> List[List[float]]:
    model = get_embedder()
    vectors = model.encode(texts, normalize_embeddings=True) if hasattr(model, "encode") else model.encode(texts)
    return [list(map(float, v)) for v in vectors]


@lru_cache(maxsize=1)
def get_chroma_client():
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    return chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)


def get_collection(department_code: str):
    client = get_chroma_client()
    return client.get_or_create_collection(name=f"dept_{department_code.lower()}")


def ingest_document(department_code: str, document_id: int, document_title: str, text: str) -> int:
    chunks = chunk_text(text)
    if not chunks:
        return 0
    vectors = embed(chunks)
    collection = get_collection(department_code)
    ids = [f"doc{document_id}_chunk{i}" for i in range(len(chunks))]
    metadatas = [{"document_id": document_id, "document_title": document_title, "chunk_index": i}
                 for i in range(len(chunks))]
    collection.upsert(ids=ids, embeddings=vectors, documents=chunks, metadatas=metadatas)
    return len(chunks)


def delete_document(department_code: str, document_id: int):
    collection = get_collection(department_code)
    collection.delete(where={"document_id": document_id})


def retrieve(department_code: str, query: str, top_k: int = None) -> List[dict]:
    top_k = top_k or settings.RAG_TOP_K
    collection = get_collection(department_code)
    if collection.count() == 0:
        return []
    query_vec = embed([query])[0]
    results = collection.query(query_embeddings=[query_vec], n_results=min(top_k, collection.count()))

    hits = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]
    for doc_text, meta, dist in zip(docs, metas, dists):
        score = max(0.0, 1.0 - (dist / 2.0))
        hits.append({"text": doc_text, "document_title": meta.get("document_title", "Unknown"),
                     "document_id": meta.get("document_id"), "score": round(score, 4)})
    return hits


def _template_answer(question: str, hits: List[dict]) -> str:
    if not hits:
        return ("I couldn't find anything in the approved department documents "
                "that answers this question. Please raise a ticket so an officer "
                "can help you directly.")
    top = hits[0]
    return (f"Based on \"{top['document_title']}\", here is the most relevant information:\n\n"
            f"{top['text'].strip()}\n\n"
            f"(This is a direct excerpt shown because the local AI model is unavailable. "
            f"If this doesn't fully answer your question, please raise a ticket.)")


def generate_answer(question: str, hits: List[dict]) -> Tuple[str, str]:
    if settings.LLM_PROVIDER != "ollama":
        return _template_answer(question, hits), "template"

    context = "\n\n---\n\n".join(f"[Source: {h['document_title']}]\n{h['text']}" for h in hits) \
        or "No relevant department documents were found."

    prompt = (
        "You are a helpful assistant for Indian government employees. "
        "Answer the employee's question using ONLY the context below. "
        "If the context does not contain the answer, say you don't know "
        "and suggest raising a support ticket. Be concise.\n\n"
        f"Context:\n{context}\n\nEmployee question: {question}\n\nAnswer:"
    )
    try:
        resp = httpx.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=settings.OLLAMA_TIMEOUT_SECONDS,
        )
        resp.raise_for_status()
        data = resp.json()
        answer = (data.get("response") or "").strip()
        if not answer:
            raise ValueError("Empty response from Ollama")
        return answer, "ollama"
    except Exception as e:  # pragma: no cover - environment dependent
        logger.warning("Ollama generation failed (%s); using template fallback.", e)
        return _template_answer(question, hits), "template"
