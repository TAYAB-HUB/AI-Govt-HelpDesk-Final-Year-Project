from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.models.models import Department, User, RoleEnum
from app.schemas.schemas import DepartmentCreate, DepartmentOut
from app.services.audit_service import log_action

router = APIRouter(prefix="/api/departments", tags=["departments"])


@router.get("", response_model=List[DepartmentOut])
def list_departments(db: Session = Depends(get_db)):
    # Intentionally public (no auth) -- the registration page needs this list
    # before the new employee has a token, and department names/descriptions
    # are not sensitive information.
    return db.query(Department).order_by(Department.name).all()


@router.post("", response_model=DepartmentOut, status_code=201)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db),
                       current_user: User = Depends(require_roles(RoleEnum.SUPER_ADMIN))):
    if db.query(Department).filter(Department.code == payload.code).first():
        raise HTTPException(status_code=400, detail="Department code already exists")
    dept = Department(**payload.model_dump())
    db.add(dept)
    db.commit()
    db.refresh(dept)
    log_action(db, current_user.id, "department.create", "department", dept.id, dept.name)
    return dept
