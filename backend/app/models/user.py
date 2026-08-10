from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from app.models.base import Base


class RoleEnum(str, Enum):
    EMPLOYEE = "Employee"
    OFFICER = "Officer"
    DEPT_ADMIN = "DeptAdmin"
    SUPER_ADMIN = "SuperAdmin"


class TicketStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "InProgress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class TicketPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"


class FeedbackVote(str, Enum):
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    employee_id = Column(String(50), nullable=True)
    role = Column(String(50), nullable=False)  # Employee, Officer, DeptAdmin, SuperAdmin
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
    
    # Relationships
    department = relationship("Department", back_populates="users")
    tickets_created = relationship("Ticket", foreign_keys="Ticket.created_by", back_populates="creator")
    tickets_assigned = relationship("Ticket", foreign_keys="Ticket.assigned_to", back_populates="assignee")
    chat_history = relationship("ChatHistory", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")