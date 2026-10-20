from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

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

@router.get("/", response_model=List[TicketResponse])
def get_all_tickets(
    status: Optional[str] = None,
    department_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Get all tickets. Employees see their own; Officers, HR, and Admins see all."""
    if current_user.role == "Employee":
        return TicketService.get_user_tickets(db, current_user.id)
    return TicketService.get_all_tickets(db, status=status, department_id=department_id)

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
    """Get all tickets for a department."""
    return TicketService.get_department_tickets(db, department_id, status)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Get a specific ticket by ID. Officers and Admins can view any ticket."""
    ticket = TicketService.get_ticket_by_id(db, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Check access permissions: Employees can only view their own
    if current_user.role == "Employee" and ticket.created_by != current_user.id:
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
    """Update a ticket (any Officer, HR Admin, or SuperAdmin)."""
    ticket = TicketService.get_ticket_by_id(db, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
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
    """Add an answer/comment to a ticket. Officers/Admins can also update ticket status."""
    ticket = TicketService.get_ticket_by_id(db, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    # Check access permissions for employees
    if current_user.role == "Employee" and ticket.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # If officer/HR/admin provided a status update, apply it
    if comment_data.status and current_user.role in ["Officer", "DeptAdmin", "SuperAdmin"]:
        ticket.status = comment_data.status
        if comment_data.status == "Resolved":
            ticket.resolved_at = datetime.utcnow()
        elif comment_data.status == "Closed":
            ticket.closed_at = datetime.utcnow()
        if not ticket.assigned_to:
            ticket.assigned_to = current_user.id
        db.commit()

    comment = TicketService.add_comment(db, ticket_id, current_user.id, comment_data)
    
    return CommentResponse(
        id=comment.id,
        ticket_id=comment.ticket_id,
        user_id=comment.user_id,
        user_name=current_user.full_name,
        user_role=current_user.role,
        comment=comment.comment,
        is_internal=comment.is_internal,
        created_at=comment.created_at
    )

@router.get("/{ticket_id}/comments", response_model=List[CommentResponse])
def get_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_employee)
):
    """Get all comments/answers for a ticket."""
    ticket = TicketService.get_ticket_by_id(db, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    # Employees can only see comments for their own ticket
    if current_user.role == "Employee" and ticket.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    comments = TicketService.get_ticket_comments(db, ticket_id)
    
    result = []
    for c in comments:
        # Filter internal comments for non-officers
        if current_user.role == "Employee" and c.is_internal:
            continue
        result.append(CommentResponse(
            id=c.id,
            ticket_id=c.ticket_id,
            user_id=c.user_id,
            user_name=c.user.full_name if c.user else "Staff",
            user_role=c.user.role if c.user else "Officer",
            comment=c.comment,
            is_internal=c.is_internal,
            created_at=c.created_at
        ))
    
    return result
