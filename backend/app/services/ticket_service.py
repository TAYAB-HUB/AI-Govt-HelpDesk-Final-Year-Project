"""
Ticket Service - Business logic for ticket management
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import random
import string

from app.models.ticket import Ticket, TicketComment
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketUpdate, CommentCreate

class TicketService:
    @staticmethod
    def generate_ticket_number() -> str:
        """Generate a unique ticket number like TKT-2024-ABCD1234."""
        year = datetime.now().year
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"TKT-{year}-{random_part}"
    
    @staticmethod
    def create_ticket(db: Session, ticket_data: TicketCreate, user_id: int) -> Ticket:
        """Create a new ticket."""
        ticket_number = TicketService.generate_ticket_number()
        
        ticket = Ticket(
            ticket_number=ticket_number,
            title=ticket_data.title,
            description=ticket_data.description,
            category=ticket_data.category,
            priority=ticket_data.priority,
            department_id=ticket_data.department_id,
            created_by=user_id,
            status="Open"
        )
        
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket
    
    @staticmethod
    def get_ticket_by_id(db: Session, ticket_id: int) -> Optional[Ticket]:
        """Get a ticket by ID."""
        return db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    @staticmethod
    def get_user_tickets(db: Session, user_id: int) -> List[Ticket]:
        """Get all tickets created by a user."""
        return db.query(Ticket).filter(Ticket.created_by == user_id).order_by(Ticket.created_at.desc()).all()
    
    @staticmethod
    def get_assigned_tickets(db: Session, user_id: int) -> List[Ticket]:
        """Get all tickets assigned to a user (officer)."""
        return db.query(Ticket).filter(Ticket.assigned_to == user_id).order_by(Ticket.created_at.desc()).all()
    
    @staticmethod
    def get_department_tickets(db: Session, department_id: int, status: Optional[str] = None) -> List[Ticket]:
        """Get all tickets for a department, optionally filtered by status."""
        query = db.query(Ticket).filter(Ticket.department_id == department_id)
        if status:
            query = query.filter(Ticket.status == status)
        return query.order_by(Ticket.created_at.desc()).all()
    
    @staticmethod
    def update_ticket(db: Session, ticket_id: int, ticket_data: TicketUpdate) -> Ticket:
        """Update a ticket."""
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            return None
        
        update_data = ticket_data.dict(exclude_unset=True)
        
        # Handle status transitions
        if 'status' in update_data:
            if update_data['status'] == 'Resolved':
                ticket.resolved_at = datetime.utcnow()
            elif update_data['status'] == 'Closed':
                ticket.closed_at = datetime.utcnow()
        
        for key, value in update_data.items():
            setattr(ticket, key, value)
        
        db.commit()
        db.refresh(ticket)
        return ticket
    
    @staticmethod
    def add_comment(db: Session, ticket_id: int, user_id: int, comment_data: CommentCreate) -> TicketComment:
        """Add a comment to a ticket."""
        comment = TicketComment(
            ticket_id=ticket_id,
            user_id=user_id,
            comment=comment_data.comment,
            is_internal=comment_data.is_internal
        )
        
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment
    
    @staticmethod
    def get_ticket_comments(db: Session, ticket_id: int) -> List[TicketComment]:
        """Get all comments for a ticket."""
        return db.query(TicketComment).filter(
            TicketComment.ticket_id == ticket_id
        ).order_by(TicketComment.created_at.asc()).all()