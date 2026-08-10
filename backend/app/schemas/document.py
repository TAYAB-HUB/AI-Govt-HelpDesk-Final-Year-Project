from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    department_id: int

class DocumentResponse(DocumentBase):
    id: int
    filename: str
    file_type: str
    file_size: int
    department_id: int
    uploaded_by: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True