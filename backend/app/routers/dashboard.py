from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles
from backend.app.models.user import Ticket, Document, ChatLog, User, RoleEnum

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/analytics")
def analytics(department_id: int = None, db: Session = Depends(get_db),
              current_user: User = Depends(require_roles(RoleEnum.DEPT_ADMIN, RoleEnum.OFFICER))):
    dept_id = department_id if current_user.role == RoleEnum.SUPER_ADMIN else current_user.department_id

    tickets_q = db.query(Ticket)
    docs_q = db.query(Document)
    chats_q = db.query(ChatLog)
    if dept_id:
        tickets_q = tickets_q.filter(Ticket.department_id == dept_id)
        docs_q = docs_q.filter(Document.department_id == dept_id)
        chats_q = chats_q.filter(ChatLog.department_id == dept_id)

    tickets = tickets_q.all()
    tickets_by_status = dict(Counter(t.status.value for t in tickets))
    tickets_by_category = dict(Counter(t.category for t in tickets))
    common_questions = [q for q, _ in Counter(c.question.strip().lower() for c in chats_q.all()).most_common(10)]

    return {"tickets_by_status": tickets_by_status, "tickets_by_category": tickets_by_category,
            "total_tickets": len(tickets), "total_documents": docs_q.count(),
            "total_chats": chats_q.count(), "common_questions": common_questions}
