import hashlib
from pathlib import Path
from typing import Iterable, List

from rag_platform.chunking import Chunk, chunk_text


SUPPORTED_EXTENSIONS = {".md", ".txt"}


def discover_documents(path: Path) -> List[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in SUPPORTED_EXTENSIONS else []
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    return sorted(
        candidate
        for candidate in path.rglob("*")
        if candidate.is_file() and candidate.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def read_document(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fingerprint_document(path: Path, content: str) -> str:
    digest = hashlib.sha256()
    digest.update(str(path).encode("utf-8"))
    digest.update(content.encode("utf-8"))
    return digest.hexdigest()


def build_chunks(
    documents: Iterable[Path], root: Path, chunk_size: int, chunk_overlap: int
) -> List[Chunk]:
    chunks: List[Chunk] = []
    for document in documents:
        text = read_document(document)
        relative_path = str(document.relative_to(root)) if root.is_dir() else document.name
        chunks.extend(chunk_text(text, relative_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap))
    return chunks
