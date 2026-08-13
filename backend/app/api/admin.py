from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import allow_officer, get_password_hash
from app.models.department import Department
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/admin", tags=["Administration"])


@router.post("/employees", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
    employee_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_officer),
):
    """Create an Employee account for the current administrator's permitted department."""
    requested_department_id = employee_data.department_id

    # Officers and department admins may only add employees in their own department.
    if current_user.role != "SuperAdmin":
        if not current_user.department_id:
            raise HTTPException(status_code=400, detail="Your account is not assigned to a department")
        if requested_department_id and requested_department_id != current_user.department_id:
            raise HTTPException(status_code=403, detail="You can only add employees to your own department")
        requested_department_id = current_user.department_id

    if not requested_department_id:
        raise HTTPException(status_code=422, detail="A department is required for an employee account")

    if not db.query(Department).filter(Department.id == requested_department_id, Department.is_active == True).first():
        raise HTTPException(status_code=404, detail="Department not found or inactive")

    if db.query(User).filter(User.email == employee_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    employee = User(
        email=employee_data.email,
        hashed_password=get_password_hash(employee_data.password),
        full_name=employee_data.full_name.strip(),
        employee_id=employee_data.employee_id,
        role="Employee",
        department_id=requested_department_id,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
