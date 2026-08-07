"""
Central application configuration, loaded from environment variables (.env).
ASSUMPTION: Default DB is SQLite for zero-friction local dev (allowed by the
project plan as a fallback). docker-compose.yml overrides DATABASE_URL to
point at the Postgres service, per spec ("Docker Compose should default to
Postgres").
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "AI Government Helpdesk (Academic Prototype)"
    ENV: Literal["dev", "docker", "prod"] = "dev"

    DATABASE_URL: str = "sqlite:///./helpdesk.db"

    JWT_SECRET_KEY: str = "CHANGE_ME_dev_only_secret_do_not_use_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8

    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:19006,http://127.0.0.1:19006"

    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    CHROMA_PERSIST_DIR: str = "./chroma_store"
    RAG_TOP_K: int = 4
    RAG_SIMILARITY_THRESHOLD: float = 0.35
    CHUNK_SIZE_CHARS: int = 800
    CHUNK_OVERLAP_CHARS: int = 120

    LLM_PROVIDER: Literal["ollama", "template"] = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"
    OLLAMA_TIMEOUT_SECONDS: int = 30

    DEMO_DATA_DIR: str = "../demo-data"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
