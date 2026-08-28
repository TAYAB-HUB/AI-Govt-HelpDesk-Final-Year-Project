from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.models.base import Base
import app.models

from app.api import admin, auth, chat, tickets, documents, departments, analytics

# Create database tables automatically
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Table creation info: {e}")

def auto_seed_db():
    db = SessionLocal()
    try:
        from app.models.user import User
        if db.query(User).count() == 0:
            import sys
            from pathlib import Path
            backend_dir = str(Path(__file__).parent.parent)
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)
            from seed import seed_departments, seed_users
            departments = seed_departments(db)
            seed_users(db, departments)
    except Exception as e:
        print(f"Auto-seed warning: {e}")
    finally:
        db.close()

try:
    auto_seed_db()
except Exception as e:
    print(f"Auto-seed error: {e}")

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered multi-department helpdesk for government employees",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(tickets.router)
app.include_router(documents.router)
app.include_router(departments.router)
app.include_router(analytics.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {
        "message": "AI Government Helpdesk API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
