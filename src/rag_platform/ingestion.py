from pathlib import Path
from dataclasses import dataclass


@dataclass
class Document:
    source: str
    text: str


def load_text_file(path: Path) -> Document:
    return Document(source=str(path), text=path.read_text(encoding="utf-8"))


def load_directory(path: str) -> list[Document]:
    root = Path(path)
    documents: list[Document] = []
    for file_path in root.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in {".txt", ".md"}:
            documents.append(load_text_file(file_path))
    return documents
