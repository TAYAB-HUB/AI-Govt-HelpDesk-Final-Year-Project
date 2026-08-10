from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from pathlib import Path

from app.core.database import get_db
from app.core.security import get_current_user, allow_dept_admin
from app.core.config import settings
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentResponse, DocumentCreate
from app.services.rag_service import rag_service
from app.services.audit_service import AuditService

router = APIRouter(prefix="/documents", tags=["Documents"])

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: str = None,
    description: str = None,
    department_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_dept_admin)
):
    """
    Upload a document (PDF/TXT) for a department.
    Only Department Admins and Super Admins can upload.
    """
    # Validate file type
    allowed_extensions = ['.pdf', '.txt', '.md']
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Check file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    max_size = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE_MB}MB"
        )
    
    # Use user's department if not specified
    if department_id is None:
        department_id = current_user.department_id
    
    # Check permissions
    if current_user.role == "DeptAdmin" and current_user.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot upload to other departments"
        )
    
    # Save file
    dept_dir = Path(settings.UPLOAD_DIR) / f"dept_{department_id}"
    dept_dir.mkdir(exist_ok=True)
    
    file_path = dept_dir / file.filename
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Create document record
    doc_title = title or file.filename
    document = Document(
        title=doc_title,
        filename=file.filename,
        file_path=str(file_path),
        file_type=file_ext[1:],  # Remove the dot
        file_size=file_size,
        department_id=department_id,
        uploaded_by=current_user.id,
        description=description
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Ingest into RAG system
    try:
        num_chunks = rag_service.ingest_document(
            document_id=document.id,
            department_id=department_id,
            file_path=str(file_path),
            title=doc_title,
            file_type=document.file_type
        )
        print(f"✅ Ingested document {document.id} into {num_chunks} chunks")
    except Exception as e:
        print(f"⚠️  Failed to ingest document: {e}")
        # Document is still saved, just not indexed
    
    # Log audit
    AuditService.log(
        db=db,
        user_id=current_user.id,
        action="UPLOAD_DOCUMENT",
        entity_type="Document",
        entity_id=document.id,
        details={"filename": file.filename, "department_id": department_id}
    )
    
    return document

@router.get("/department/{department_id}", response_model=List[DocumentResponse])
def get_department_documents(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all documents for a department."""
    documents = db.query(Document).filter(
        Document.department_id == department_id,
        Document.is_active == True
    ).order_by(Document.created_at.desc()).all()
    
    return documents

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_dept_admin)
):
    """Delete a document (soft delete)."""
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check permissions
    if current_user.role == "DeptAdmin" and current_user.department_id != document.department_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete documents from other departments"
        )
    
    # Soft delete
    document.is_active = False
    db.commit()
    
    # Remove from vector store
    try:
        rag_service.delete_document_from_index(document.id, document.department_id)
    except Exception as e:
        print(f"⚠️  Failed to remove from index: {e}")
    
    # Log audit
    AuditService.log(
        db=db,
        user_id=current_user.id,
        action="DELETE_DOCUMENT",
        entity_type="Document",
        entity_id=document_id,
        details={"filename": document.filename}
    )
    
    return None