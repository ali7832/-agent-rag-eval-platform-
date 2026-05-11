import json
from pathlib import Path
from typing import List

from rag_platform.schemas import EvaluationExampleResult, EvaluationResponse


def load_eval_dataset(dataset_path: Path) -> List[dict]:
    lines = dataset_path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def grounded(answer: str, retrieved_sources: List[str], expected_sources: List[str]) -> bool:
    if not answer.strip():
        return False
    return any(source in retrieved_sources for source in expected_sources)


def build_evaluation_response(results: List[EvaluationExampleResult]) -> EvaluationResponse:
    examples = len(results)
    hit_rate = (
        sum(1 for result in results if result.matched_expected_sources > 0) / examples if examples else 0.0
    )
    grounded_rate = sum(1 for result in results if result.grounded) / examples if examples else 0.0
    return EvaluationResponse(
        examples=examples,
        retrieval_hit_rate=round(hit_rate, 3),
        grounded_rate=round(grounded_rate, 3),
        results=results,
    )
