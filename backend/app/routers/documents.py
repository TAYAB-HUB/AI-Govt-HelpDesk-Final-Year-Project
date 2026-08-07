import os
import shutil
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_roles, get_current_user, same_department_or_admin
from app.models.models import Document, Department, User, RoleEnum
from app.schemas.schemas import DocumentOut
from app.services import rag_service
from app.services.audit_service import log_action

router = APIRouter(prefix="/api/documents", tags=["documents"])

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("", response_model=List[DocumentOut])
def list_documents(department_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    if not same_department_or_admin(current_user, department_id):
        raise HTTPException(status_code=403, detail="Not permitted to view this department's documents")
    return db.query(Document).filter(Document.department_id == department_id).all()


@router.post("/upload", response_model=DocumentOut, status_code=201)
def upload_document(department_id: int, title: str, file: UploadFile = File(...),
                     db: Session = Depends(get_db),
                     current_user: User = Depends(require_roles(RoleEnum.DEPT_ADMIN))):
    dept = db.query(Department).filter(Department.id == department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "txt"
    if ext not in ("pdf", "txt", "md"):
        raise HTTPException(status_code=400, detail="Only PDF, TXT, or MD files are supported")

    saved_name = f"{uuid.uuid4().hex}_{file.filename}"
    saved_path = os.path.join(UPLOAD_DIR, saved_name)
    with open(saved_path, "wb") as out:
        shutil.copyfileobj(file.file, out)

    text = rag_service.extract_text(saved_path, file.filename)

    doc = Document(department_id=department_id, title=title, filename=file.filename,
                    source_type="upload", raw_text_char_count=len(text),
                    uploaded_by_id=current_user.id)
    db.add(doc)
    db.commit()
    db.refresh(doc)

    chunk_count = rag_service.ingest_document(dept.code, doc.id, doc.title, text)
    doc.chunk_count = chunk_count
    db.commit()
    db.refresh(doc)

    log_action(db, current_user.id, "document.upload", "document", doc.id,
               f"{doc.title} ({chunk_count} chunks) into department {dept.code}")
    return doc


@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(require_roles(RoleEnum.DEPT_ADMIN))):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    dept = db.query(Department).filter(Department.id == doc.department_id).first()
    rag_service.delete_document(dept.code, doc.id)
    db.delete(doc)
    db.commit()
    log_action(db, current_user.id, "document.delete", "document", document_id, doc.title)
