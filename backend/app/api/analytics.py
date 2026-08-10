from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any

from app.core.database import get_db
from app.core.security import get_current_user, allow_officer
from app.models.user import User
from app.models.ticket import Ticket
from app.models.chat import ChatHistory, ChatFeedback

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard", response_model=Dict[str, Any])
def get_dashboard_stats(
    department_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_officer)
):
    """
    Get analytics for dashboard.
    Officers see their department, Super Admin sees all.
    """
    # Determine which department(s) to query
    if current_user.role == "SuperAdmin":
        dept_filter = department_id if department_id else None
    else:
        dept_filter = current_user.department_id
    
    # Ticket statistics
    ticket_query = db.query(Ticket)
    if dept_filter:
        ticket_query = ticket_query.filter(Ticket.department_id == dept_filter)
    
    total_tickets = ticket_query.count()
    open_tickets = ticket_query.filter(Ticket.status == "Open").count()
    in_progress_tickets = ticket_query.filter(Ticket.status == "InProgress").count()
    resolved_tickets = ticket_query.filter(Ticket.status == "Resolved").count()
    closed_tickets = ticket_query.filter(Ticket.status == "Closed").count()
    
    # Tickets by priority
    priority_stats = db.query(
        Ticket.priority,
        func.count(Ticket.id).label('count')
    ).filter(
        Ticket.department_id == dept_filter if dept_filter else True
    ).group_by(Ticket.priority).all()
    
    # Chat statistics
    chat_query = db.query(ChatHistory)
    if dept_filter:
        chat_query = chat_query.filter(ChatHistory.department_id == dept_filter)
    
    total_chats = chat_query.count()
    avg_confidence = db.query(func.avg(ChatHistory.confidence_score)).filter(
        ChatHistory.department_id == dept_filter if dept_filter else True
    ).scalar() or 0
    
    # Feedback stats
    feedback_stats = db.query(
        ChatFeedback.feedback_type,
        func.count(ChatFeedback.id).label('count')
    ).join(ChatHistory).filter(
        ChatHistory.department_id == dept_filter if dept_filter else True
    ).group_by(ChatFeedback.feedback_type).all()
    
    return {
        "tickets": {
            "total": total_tickets,
            "open": open_tickets,
            "in_progress": in_progress_tickets,
            "resolved": resolved_tickets,
            "closed": closed_tickets,
            "by_priority": {stat.priority: stat.count for stat in priority_stats}
        },
        "chat": {
            "total_interactions": total_chats,
            "avg_confidence": round(float(avg_confidence), 2),
            "feedback": {stat.feedback_type: stat.count for stat in feedback_stats}
        }
    }

@router.get("/tickets-trend", response_model=Dict[str, Any])
def get_tickets_trend(
    days: int = 30,
    department_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_officer)
):
    """Get ticket creation trend over time."""
    # This is a simplified version - you'd want to group by date
    dept_filter = department_id if current_user.role == "SuperAdmin" else current_user.department_id
    
    tickets = db.query(
        func.date(Ticket.created_at).label('date'),
        func.count(Ticket.id).label('count')
    ).filter(
        Ticket.department_id == dept_filter if dept_filter else True
    ).group_by(func.date(Ticket.created_at)).order_by(func.date(Ticket.created_at).desc()).limit(days).all()
    
    return {
        "trend": [{"date": str(t.date), "count": t.count} for t in tickets]
    }