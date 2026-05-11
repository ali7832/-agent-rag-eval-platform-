import re
from dataclasses import dataclass
from typing import Iterable, List


TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9_]+")


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    source_path: str
    score: float
    content: str


def tokenize(text: str) -> List[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def score_chunk(question: str, chunk_content: str) -> float:
    query_tokens = tokenize(question)
    chunk_tokens = tokenize(chunk_content)
    if not query_tokens or not chunk_tokens:
        return 0.0

    query_set = set(query_tokens)
    chunk_set = set(chunk_tokens)
    overlap = query_set & chunk_set
    coverage = len(overlap) / len(query_set)
    density = sum(chunk_tokens.count(token) for token in overlap) / len(chunk_tokens)
    return round((coverage * 0.8) + (density * 0.2), 4)


def rank_chunks(question: str, rows: Iterable[object], top_k: int) -> List[RetrievedChunk]:
    ranked = []
    for row in rows:
        score = score_chunk(question, row["content"])
        if score <= 0:
            continue
        ranked.append(
            RetrievedChunk(
                chunk_id=row["chunk_id"],
                source_path=row["source_path"],
                score=score,
                content=row["content"],
            )
        )
    ranked.sort(key=lambda chunk: chunk.score, reverse=True)
    return ranked[:top_k]
