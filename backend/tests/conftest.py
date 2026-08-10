import os
import sys
import tempfile

import pytest
from fastapi.testclient import TestClient

# Point the app at a throwaway SQLite DB + Chroma dir BEFORE importing app.main
TEST_DIR = tempfile.mkdtemp(prefix="helpdesk_test_")
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DIR}/test.db"
os.environ["CHROMA_PERSIST_DIR"] = f"{TEST_DIR}/chroma"
os.environ["LLM_PROVIDER"] = "template"  # never hit a real Ollama server in tests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app  # noqa: E402
from app.core.database import SessionLocal  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from backend.app.models.user import Department, User, RoleEnum  # noqa: E402


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def seed_minimal_data():
    db = SessionLocal()
    hr = Department(name="Human Resources", code="HR", description="test")
    finance = Department(name="Finance", code="FINANCE", description="test")
    db.add_all([hr, finance])
    db.commit()

    users = [
        User(full_name="Employee", email="employee@test.example.com", hashed_password=hash_password("Pass@1234"),
             role=RoleEnum.EMPLOYEE, department_id=hr.id),
        User(full_name="Officer", email="officer@test.example.com", hashed_password=hash_password("Pass@1234"),
             role=RoleEnum.OFFICER, department_id=hr.id),
        User(full_name="DeptAdmin", email="deptadmin@test.example.com", hashed_password=hash_password("Pass@1234"),
             role=RoleEnum.DEPT_ADMIN, department_id=hr.id),
        User(full_name="SuperAdmin", email="superadmin@test.example.com", hashed_password=hash_password("Pass@1234"),
             role=RoleEnum.SUPER_ADMIN, department_id=None),
        User(full_name="FinanceEmployee", email="fin.employee@test.example.com", hashed_password=hash_password("Pass@1234"),
             role=RoleEnum.EMPLOYEE, department_id=finance.id),
    ]
    db.add_all(users)
    db.commit()
    db.close()
    yield


def login(client, email, password="Pass@1234"):
    resp = client.post("/api/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}
