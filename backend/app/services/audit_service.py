from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import AuditLog


def log_action(db: Session, actor_id: Optional[int], action: str, target_type: str = "",
               target_id: Optional[int] = None, detail: str = ""):
    entry = AuditLog(actor_id=actor_id, action=action, target_type=target_type,
                      target_id=target_id, detail=detail)
    db.add(entry)
    db.commit()
    return entry
