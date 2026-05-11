from typing import List

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    path: str = Field(..., description="Directory or file path to ingest.")


class IngestResponse(BaseModel):
    files_indexed: int
    chunks_indexed: int


class SearchResult(BaseModel):
    chunk_id: str
    source_path: str
    score: float
    content: str


class QueryRequest(BaseModel):
    question: str
    top_k: int = Field(default=4, ge=1, le=20)


class Citation(BaseModel):
    chunk_id: str
    source_path: str
    score: float
    snippet: str


class QueryResponse(BaseModel):
    question: str
    answer: str
    citations: List[Citation]


class EvaluationRequest(BaseModel):
    dataset_path: str


class EvaluationExampleResult(BaseModel):
    question: str
    answer: str
    matched_expected_sources: int
    expected_sources: List[str]
    retrieved_sources: List[str]
    grounded: bool


class EvaluationResponse(BaseModel):
    examples: int
    retrieval_hit_rate: float
    grounded_rate: float
    results: List[EvaluationExampleResult]


class HealthResponse(BaseModel):
    status: str
