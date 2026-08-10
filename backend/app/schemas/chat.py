from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    question: str
    department_id: int

class ChatSource(BaseModel):
    document_title: str
    snippet: str
    page: Optional[int] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[ChatSource]
    confidence_score: float
    suggest_ticket: bool = False

class ChatHistoryResponse(BaseModel):
    id: int
    question: str
    answer: str
    sources: Optional[List[Dict[str, Any]]] = None
    confidence_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class FeedbackCreate(BaseModel):
    feedback_type: str  # thumbs_up or thumbs_down
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    chat_id: int
    feedback_type: str
    comment: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True