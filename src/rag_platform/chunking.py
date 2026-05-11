from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source_path: str
    content: str
    position: int


def chunk_text(text: str, source_path: str, chunk_size: int, chunk_overlap: int) -> List[Chunk]:
    normalized = " ".join(text.split())
    if not normalized:
        return []

    chunks: List[Chunk] = []
    step = max(1, chunk_size - chunk_overlap)
    start = 0
    index = 0

    while start < len(normalized):
        end = min(len(normalized), start + chunk_size)
        content = normalized[start:end].strip()
        if content:
            chunks.append(
                Chunk(
                    chunk_id=f"{source_path}:{index}",
                    source_path=source_path,
                    content=content,
                    position=index,
                )
            )
        if end == len(normalized):
            break
        start += step
        index += 1

    return chunks
