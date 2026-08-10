"""
Seeds the database with demo departments, demo users (one per role, all
obviously-fake credentials), and ingests the sample department documents
from /demo-data into the RAG vector store.

Run with:  python -m app.seed.seed
Safe to re-run: it skips creation if data already exists.
"""
import os
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import SessionLocal, engine
from app.core.security import hash_password
from app.models.base import Base
from app.models.department import Department
from app.models.user import User, RoleEnum
from app.models.document import Document
from app.models.ticket import Ticket, TicketComment
from app.models.chat import ChatHistory, ChatFeedback
from app.models.audit import AuditLog
from app.services import rag_service

DEPARTMENTS = [
    {"name": "Human Resources", "code": "HR", "description": "Leave, recruitment, onboarding, appraisals"},
    {"name": "Finance", "code": "FINANCE", "description": "Salary, reimbursement, budget and procurement"},
    {"name": "Information Technology", "code": "IT", "description": "IT helpdesk, accounts, assets"},
    {"name": "Pension", "code": "PENSION", "description": "Retirement, pension processing, PPO"},
    {"name": "Administration", "code": "ADMIN", "description": "Office facilities, travel, maintenance"},
]

# Demo credentials are intentionally obvious/fake -- printed in README too.
DEMO_PASSWORD = "Demo@1234"

DEMO_USERS = [
    {"full_name": "Employee Demo", "email": "employee@demo.gov.in", "role": RoleEnum.EMPLOYEE, "dept": "HR"},
    {"full_name": "Officer Demo", "email": "officer@demo.gov.in", "role": RoleEnum.OFFICER, "dept": "HR"},
    {"full_name": "Dept Admin Demo", "email": "deptadmin@demo.gov.in", "role": RoleEnum.DEPT_ADMIN, "dept": "HR"},
    {"full_name": "Super Admin Demo", "email": "superadmin@demo.gov.in", "role": RoleEnum.SUPER_ADMIN, "dept": None},
    {"full_name": "Finance Officer Demo", "email": "finance.officer@demo.gov.in", "role": RoleEnum.OFFICER, "dept": "FINANCE"},
    {"full_name": "IT Officer Demo", "email": "it.officer@demo.gov.in", "role": RoleEnum.OFFICER, "dept": "IT"},
    {"full_name": "Pension Officer Demo", "email": "pension.officer@demo.gov.in", "role": RoleEnum.OFFICER, "dept": "PENSION"},
    {"full_name": "Admin Officer Demo", "email": "admin.officer@demo.gov.in", "role": RoleEnum.OFFICER, "dept": "ADMIN"},
]

FOLDER_TO_DEPT = {
    "hr": "HR",
    "finance": "FINANCE",
    "it": "IT",
    "pension": "PENSION",
    "admin": "ADMIN",
}


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        dept_by_code = {}
        for d in DEPARTMENTS:
            existing = db.query(Department).filter(Department.code == d["code"]).first()
            if existing:
                dept_by_code[d["code"]] = existing
                continue
            dept = Department(**d)
            db.add(dept)
            db.commit()
            db.refresh(dept)
            dept_by_code[d["code"]] = dept
            print(f"[seed] created department {dept.code}")

        for u in DEMO_USERS:
            existing = db.query(User).filter(User.email == u["email"]).first()
            if existing:
                continue
            dept_id = dept_by_code[u["dept"]].id if u["dept"] else None
            user = User(
                full_name=u["full_name"],
                email=u["email"],
                hashed_password=hash_password(DEMO_PASSWORD),
                role=u["role"],
                department_id=dept_id,
            )
            db.add(user)
            print(f"[seed] created user {user.email} ({user.role.value})")
        db.commit()

        demo_data_root = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "..", "demo-data")
        )

        for folder, dept_code in FOLDER_TO_DEPT.items():
            dept = dept_by_code[dept_code]
            folder_path = os.path.join(demo_data_root, folder)
            for path in sorted(glob.glob(os.path.join(folder_path, "*.md"))):
                filename = os.path.basename(path)
                existing_doc = (
                    db.query(Document)
                    .filter(Document.department_id == dept.id, Document.filename == filename)
                    .first()
                )
                if existing_doc:
                    continue
                text = rag_service.extract_text(path, filename)
                title = filename.replace(".md", "").replace("-", " ").title()
                doc = Document(
                    department_id=dept.id,
                    title=title,
                    filename=filename,
                    source_type="seed",
                    raw_text_char_count=len(text),
                )
                db.add(doc)
                db.commit()
                db.refresh(doc)
                chunk_count = rag_service.ingest_document(dept.code, doc.id, doc.title, text)
                doc.chunk_count = chunk_count
                db.commit()
                print(f"[seed] ingested {filename} into {dept.code} ({chunk_count} chunks)")

        print("\n[seed] Done. Demo login password for all seeded users:", DEMO_PASSWORD)
    finally:
        db.close()


if __name__ == "__main__":
    seed()
