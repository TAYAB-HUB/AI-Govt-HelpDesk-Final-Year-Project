from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketBase(BaseModel):
    title: str
    description: str
    category: str
    priority: str
    department_id: int

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None

class TicketResponse(TicketBase):
    id: int
    ticket_number: str
    status: str
    created_by: int
    assigned_to: Optional[int] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    comment: str
    is_internal: bool = False

class CommentResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    comment: str
    is_internal: bool
    created_at: datetime
    
    class Config:
        from_attributes = True