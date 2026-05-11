from dataclasses import dataclass


@dataclass
class EvaluationResult:
    grounded: bool
    score: float
    feedback: str


class GroundednessEvaluator:
    def evaluate(self, answer: str, context: str) -> EvaluationResult:
        grounded = any(token in context.lower() for token in answer.lower().split())
        score = 1.0 if grounded else 0.25
        feedback = "Grounded response" if grounded else "Potential hallucination"
        return EvaluationResult(grounded=grounded, score=score, feedback=feedback)
