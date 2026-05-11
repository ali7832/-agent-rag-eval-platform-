import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str = "Agent RAG Evaluation Platform"
    database_path: Path = Path(os.getenv("RAG_PLATFORM_DATABASE_PATH", "rag_platform.db"))
    chunk_size: int = int(os.getenv("RAG_PLATFORM_CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("RAG_PLATFORM_CHUNK_OVERLAP", "75"))
    default_top_k: int = int(os.getenv("RAG_PLATFORM_DEFAULT_TOP_K", "4"))


settings = Settings()
