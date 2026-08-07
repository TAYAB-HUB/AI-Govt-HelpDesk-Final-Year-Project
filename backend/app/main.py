from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, departments, documents, chat, tickets, dashboard, admin

# NOTE: create_all() is used for demo simplicity; the /backend/alembic folder
# holds the migration scaffold for a "real" deployment workflow as required
# by the spec. Run `alembic upgrade head` instead of relying on create_all()
# once you're managing schema changes over time.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+):(5173|19006)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(departments.router)
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(tickets.router)
app.include_router(dashboard.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}
