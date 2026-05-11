from dataclasses import dataclass
from typing import List


@dataclass
class RetrievalResult:
    document: str
    content: str
    score: float


class LexicalRetriever:
    def __init__(self) -> None:
        self.documents = [
            {
                "document": "architecture.md",
                "content": "The platform evaluates grounded retrieval augmented generation systems.",
            },
            {
                "document": "evaluation.md",
                "content": "Groundedness and citation quality are measured during evaluation.",
            },
        ]

    def search(self, query: str, top_k: int = 3) -> List[RetrievalResult]:
        scored = []
        for item in self.documents:
            overlap = len(set(query.lower().split()) & set(item['content'].lower().split()))
            score = overlap / max(len(query.split()), 1)
            scored.append(
                RetrievalResult(
                    document=item['document'],
                    content=item['content'],
                    score=round(score, 3),
                )
            )

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]
