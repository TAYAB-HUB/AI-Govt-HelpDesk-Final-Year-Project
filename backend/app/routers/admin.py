from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles
from backend.app.models.user import AuditLog, User, RoleEnum
from app.schemas.schemas import AuditLogOut, UserOut
from app.services.audit_service import log_action

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/audit-logs", response_model=List[AuditLogOut])
def list_audit_logs(limit: int = 100, db: Session = Depends(get_db),
                     _: User = Depends(require_roles(RoleEnum.SUPER_ADMIN))):
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()


@router.get("/users", response_model=List[UserOut])
def list_users(department_id: Optional[int] = None, db: Session = Depends(get_db),
                current_user: User = Depends(require_roles(RoleEnum.SUPER_ADMIN, RoleEnum.DEPT_ADMIN))):
    q = db.query(User)
    if current_user.role == RoleEnum.DEPT_ADMIN:
        q = q.filter(User.department_id == current_user.department_id)
    elif department_id:
        q = q.filter(User.department_id == department_id)
    return q.all()


@router.patch("/users/{user_id}/role", response_model=UserOut)
def change_role(user_id: int, role: RoleEnum, db: Session = Depends(get_db),
                 current_user: User = Depends(require_roles(RoleEnum.SUPER_ADMIN))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    old_role = user.role
    user.role = role
    db.commit()
    db.refresh(user)
    log_action(db, current_user.id, "user.role_change", "user", user.id, f"{old_role.value} -> {role.value}")
    return user


@router.patch("/users/{user_id}/toggle-active", response_model=UserOut)
def toggle_active(user_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(require_roles(RoleEnum.SUPER_ADMIN))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)
    log_action(db, current_user.id, "user.toggle_active", "user", user.id, str(user.is_active))
    return user
