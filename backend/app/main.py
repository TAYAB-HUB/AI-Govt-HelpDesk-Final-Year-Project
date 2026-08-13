from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

from app.api import admin, auth, chat, tickets, documents, departments, analytics

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
