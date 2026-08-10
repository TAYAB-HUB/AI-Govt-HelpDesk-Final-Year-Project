from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user, allow_employee, allow_officer
from app.models.user import User
from app.models.ticket import Ticket
from app.schemas.ticket import (
    TicketCreate, TicketUpdate, TicketResponse,
    CommentCreate, CommentResponse
)
from app.services.ticket_service import TicketService
from app.services.audit_service import AuditService

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Create a new support ticket."""
    ticket = TicketService.create_ticket(db, ticket_data, current_user.id)
    
    # Log audit
    AuditService.log(
        db=db,
        user_id=current_user.id,
        action="CREATE_TICKET",
        entity_type="Ticket",
        entity_id=ticket.id,
        details={"ticket_number": ticket.ticket_number}
    )
    
    return ticket

@router.get("/my-tickets", response_model=List[TicketResponse])
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Get all tickets created by the current user."""
    return TicketService.get_user_tickets(db, current_user.id)

@router.get("/assigned", response_model=List[TicketResponse])
def get_assigned_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_officer)
):
    """Get all tickets assigned to the current user (officer)."""
    return TicketService.get_assigned_tickets(db, current_user.id)

@router.get("/department/{department_id}", response_model=List[TicketResponse])
def get_department_tickets(
    department_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_officer)
):
    """Get all tickets for a department (officers and admins only)."""
    # Check if user has access to this department
    if current_user.role not in ["SuperAdmin"] and current_user.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this department"
        )
    
    return TicketService.get_department_tickets(db, department_id, status)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Get a specific ticket by ID."""
    ticket = TicketService.get_ticket_by_id(db, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Check access permissions
    if current_user.role == "Employee" and ticket.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if current_user.role == "Officer" and ticket.department_id != current_user.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return ticket

@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_officer)
):
    """Update a ticket (officers and admins only)."""
    ticket = TicketService.get_ticket_by_id(db, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Check permissions
    if current_user.role == "Officer" and ticket.department_id != current_user.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    updated_ticket = TicketService.update_ticket(db, ticket_id, ticket_data)
    
    # Log audit
    AuditService.log(
        db=db,
        user_id=current_user.id,
        action="UPDATE_TICKET",
        entity_type="Ticket",
        entity_id=ticket_id,
        details=ticket_data.dict(exclude_unset=True)
    )
    
    return updated_ticket

@router.post("/{ticket_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment(
    ticket_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Add a comment to a ticket."""
    ticket = TicketService.get_ticket_by_id(db, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    comment = TicketService.add_comment(db, ticket_id, current_user.id, comment_data)
    return comment

@router.get("/{ticket_id}/comments", response_model=List[CommentResponse])
def get_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Get all comments for a ticket."""
    ticket = TicketService.get_ticket_by_id(db, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    comments = TicketService.get_ticket_comments(db, ticket_id)
    
    # Filter internal comments for non-officers
    if current_user.role == "Employee":
        comments = [c for c in comments if not c.is_internal]
    
    return comments