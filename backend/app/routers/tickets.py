from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles, same_department_or_admin
from backend.app.models.user import Ticket, TicketComment, User, RoleEnum, TicketStatus
from app.schemas.schemas import TicketCreate, TicketOut, TicketCommentCreate, TicketAssign
from app.services.audit_service import log_action

router = APIRouter(prefix="/api/tickets", tags=["tickets"])


def _visible_tickets_query(db: Session, user: User):
    q = db.query(Ticket)
    if user.role == RoleEnum.EMPLOYEE:
        q = q.filter(Ticket.created_by_id == user.id)
    elif user.role in (RoleEnum.OFFICER, RoleEnum.DEPT_ADMIN):
        q = q.filter(Ticket.department_id == user.department_id)
    return q


@router.post("", response_model=TicketOut, status_code=201)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if not same_department_or_admin(current_user, payload.department_id):
        raise HTTPException(status_code=403, detail="Cannot raise a ticket for another department")
    ticket = Ticket(department_id=payload.department_id, created_by_id=current_user.id,
                     category=payload.category, subject=payload.subject,
                     description=payload.description, priority=payload.priority,
                     origin_chat_log_id=payload.origin_chat_log_id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    log_action(db, current_user.id, "ticket.create", "ticket", ticket.id, ticket.subject)
    return ticket


@router.get("", response_model=List[TicketOut])
def list_tickets(status: Optional[TicketStatus] = None, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    q = _visible_tickets_query(db, current_user)
    if status:
        q = q.filter(Ticket.status == status)
    return q.order_by(Ticket.created_at.desc()).all()


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    ticket = _visible_tickets_query(db, current_user).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found or not visible to you")
    return ticket


@router.post("/{ticket_id}/assign", response_model=TicketOut)
def assign_ticket(ticket_id: int, payload: TicketAssign, db: Session = Depends(get_db),
                   current_user: User = Depends(require_roles(RoleEnum.DEPT_ADMIN))):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.assigned_to_id = payload.assigned_to_id
    db.commit()
    db.refresh(ticket)
    log_action(db, current_user.id, "ticket.assign", "ticket", ticket.id,
               f"assigned to user {payload.assigned_to_id}")
    return ticket


@router.post("/{ticket_id}/comments", response_model=TicketOut)
def add_comment(ticket_id: int, payload: TicketCommentCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    ticket = _visible_tickets_query(db, current_user).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found or not visible to you")
    if payload.status_change_to and current_user.role == RoleEnum.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Employees cannot change ticket status")

    comment = TicketComment(ticket_id=ticket.id, author_id=current_user.id, body=payload.body,
                             status_change_to=payload.status_change_to)
    db.add(comment)

    if payload.status_change_to:
        old_status = ticket.status
        ticket.status = payload.status_change_to
        log_action(db, current_user.id, "ticket.status_change", "ticket", ticket.id,
                   f"{old_status.value} -> {payload.status_change_to.value}")

    db.commit()
    db.refresh(ticket)
    return ticket
