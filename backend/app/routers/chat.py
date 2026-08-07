import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, same_department_or_admin
from app.core.config import settings
from app.models.models import ChatLog, Department, User, Feedback
from app.schemas.schemas import ChatRequest, ChatResponse, SourceRef, FeedbackRequest
from app.services import rag_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
def ask(payload: ChatRequest, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    if not same_department_or_admin(current_user, payload.department_id):
        raise HTTPException(status_code=403, detail="Select a department you belong to")

    dept = db.query(Department).filter(Department.id == payload.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    hits = rag_service.retrieve(dept.code, payload.question)
    top_similarity = hits[0]["score"] if hits else 0.0
    answer, provider_used = rag_service.generate_answer(payload.question, hits)
    suggest_ticket = top_similarity < settings.RAG_SIMILARITY_THRESHOLD

    sources = [SourceRef(document_title=h["document_title"], snippet=h["text"][:280], score=h["score"])
               for h in hits]

    chat_log = ChatLog(user_id=current_user.id, department_id=dept.id, question=payload.question,
                        answer=answer, sources_json=json.dumps([s.model_dump() for s in sources]),
                        top_similarity=top_similarity, suggested_ticket=suggest_ticket,
                        llm_provider_used=provider_used)
    db.add(chat_log)
    db.commit()
    db.refresh(chat_log)

    return ChatResponse(chat_log_id=chat_log.id, answer=answer, sources=sources,
                         top_similarity=top_similarity, suggest_ticket=suggest_ticket,
                         llm_provider_used=provider_used)


@router.get("/history")
def history(department_id: int = None, db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):
    q = db.query(ChatLog).filter(ChatLog.user_id == current_user.id)
    if department_id:
        q = q.filter(ChatLog.department_id == department_id)
    logs = q.order_by(ChatLog.created_at.desc()).limit(50).all()
    return [{"id": l.id, "question": l.question, "answer": l.answer,
             "sources": json.loads(l.sources_json), "suggested_ticket": l.suggested_ticket,
             "created_at": l.created_at} for l in logs]


@router.post("/feedback", status_code=204)
def feedback(payload: FeedbackRequest, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    chat_log = db.query(ChatLog).filter(ChatLog.id == payload.chat_log_id).first()
    if not chat_log:
        raise HTTPException(status_code=404, detail="Chat log not found")
    fb = Feedback(chat_log_id=payload.chat_log_id, user_id=current_user.id, vote=payload.vote)
    db.add(fb)
    db.commit()
