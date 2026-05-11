from typing import List

from rag_platform.retrieval import RetrievedChunk


def build_answer(question: str, chunks: List[RetrievedChunk]) -> str:
    if not chunks:
        return (
            f"I could not find grounded evidence for: '{question}'. "
            "In a production system I would fall back to clarification or retrieval expansion."
        )

    evidence_lines = []
    for chunk in chunks[:3]:
        evidence_lines.append(f"{chunk.source_path}: {chunk.content}")

    joined = " ".join(evidence_lines)
    return (
        f"Based on the indexed corpus, the strongest evidence for '{question}' is: {joined} "
        "This answer is intentionally extractive so the reasoning stays traceable to source documents."
    )
