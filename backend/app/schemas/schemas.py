from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.models import RoleEnum, TicketStatus, TicketPriority, FeedbackVote


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    department_id: Optional[int] = None
    role: RoleEnum = RoleEnum.EMPLOYEE


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: RoleEnum
    full_name: str
    department_id: Optional[int] = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: str
    role: RoleEnum
    department_id: Optional[int] = None
    is_active: bool


class DepartmentCreate(BaseModel):
    name: str
    code: str
    description: str = ""


class DepartmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: str
    description: str


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    department_id: int
    title: str
    filename: str
    source_type: str
    chunk_count: int
    created_at: datetime


class ChatRequest(BaseModel):
    department_id: int
    question: str


class SourceRef(BaseModel):
    document_title: str
    snippet: str
    score: float


class ChatResponse(BaseModel):
    chat_log_id: int
    answer: str
    sources: List[SourceRef]
    top_similarity: float
    suggest_ticket: bool
    llm_provider_used: str


class FeedbackRequest(BaseModel):
    chat_log_id: int
    vote: FeedbackVote


class TicketCreate(BaseModel):
    department_id: int
    category: str
    subject: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM
    origin_chat_log_id: Optional[int] = None


class TicketCommentCreate(BaseModel):
    body: str
    status_change_to: Optional[TicketStatus] = None


class TicketCommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int
    body: str
    status_change_to: Optional[TicketStatus]
    created_at: datetime


class TicketAssign(BaseModel):
    assigned_to_id: int


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    department_id: int
    created_by_id: int
    assigned_to_id: Optional[int]
    category: str
    subject: str
    description: str
    priority: TicketPriority
    status: TicketStatus
    created_at: datetime
    updated_at: datetime
    comments: List[TicketCommentOut] = []


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    actor_id: Optional[int]
    action: str
    target_type: str
    target_id: Optional[int]
    detail: str
    created_at: datetime


class AnalyticsSummary(BaseModel):
    tickets_by_status: dict
    tickets_by_category: dict
    total_tickets: int
    total_documents: int
    common_questions: List[str]
