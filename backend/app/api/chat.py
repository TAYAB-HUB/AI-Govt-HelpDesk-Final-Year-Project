from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user, allow_employee
from app.models.user import User
from app.models.chat import ChatHistory, ChatFeedback
from app.schemas.chat import (
    ChatRequest, ChatResponse, ChatSource,
    ChatHistoryResponse, FeedbackCreate, FeedbackResponse
)
from app.services.rag_service import rag_service

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/ask", response_model=ChatResponse)
async def ask_question(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """
    Ask a question to the chatbot.
    Uses RAG to retrieve relevant documents and generate an answer.
    """
    # Retrieve relevant chunks
    chunks = rag_service.retrieve_relevant_chunks(
        question=request.question,
        department_id=request.department_id
    )
    
    if not chunks:
        return ChatResponse(
            answer="I don't have any relevant information to answer this question. Would you like to create a support ticket?",
            sources=[],
            confidence_score=0.0,
            suggest_ticket=True
        )
    
    # Generate answer using LLM
    answer = await rag_service.generate_answer_ollama(
        question=request.question,
        context_chunks=chunks
    )
    
    # Calculate confidence
    confidence = rag_service.calculate_confidence(chunks)
    
    # Prepare sources
    sources = [
        ChatSource(
            document_title=chunk['metadata']['document_title'],
            snippet=chunk['text'][:200] + "..."
        )
        for chunk in chunks[:3]
    ]
    
    # Save to chat history
    chat_record = ChatHistory(
        user_id=current_user.id,
        department_id=request.department_id,
        question=request.question,
        answer=answer,
        sources=[{
            "document_title": s.document_title,
            "snippet": s.snippet
        } for s in sources],
        confidence_score=confidence
    )
    db.add(chat_record)
    db.commit()
    
    # Determine if ticket should be suggested
    suggest_ticket = confidence < 0.6
    
    return ChatResponse(
        answer=answer,
        sources=sources,
        confidence_score=confidence,
        suggest_ticket=suggest_ticket
    )

@router.get("/history", response_model=List[ChatHistoryResponse])
def get_chat_history(
    department_id: int = None,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Get chat history for the current user."""
    query = db.query(ChatHistory).filter(ChatHistory.user_id == current_user.id)
    
    if department_id:
        query = query.filter(ChatHistory.department_id == department_id)
    
    history = query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
    return history

@router.post("/feedback/{chat_id}", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    chat_id: int,
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Submit feedback (thumbs up/down) for a chat response."""
    # Check if chat exists and belongs to user
    chat = db.query(ChatHistory).filter(
        ChatHistory.id == chat_id,
        ChatHistory.user_id == current_user.id
    ).first()
    
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    
    # Create feedback
    feedback = ChatFeedback(
        chat_id=chat_id,
        user_id=current_user.id,
        feedback_type=feedback_data.feedback_type,
        comment=feedback_data.comment
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return feedback