from pathlib import Path

from rag_platform.config import settings
from rag_platform.evaluation import build_evaluation_response, grounded, load_eval_dataset
from rag_platform.generation import build_answer
from rag_platform.ingestion import build_chunks, discover_documents
from rag_platform.retrieval import rank_chunks
from rag_platform.schemas import (
    Citation,
    EvaluationExampleResult,
    EvaluationResponse,
    IngestResponse,
    QueryResponse,
)
from rag_platform.storage import SQLiteChunkRepository


class RagPlatformService:
    def __init__(self, repository: SQLiteChunkRepository | None = None):
        self.repository = repository or SQLiteChunkRepository(settings.database_path)

    def ingest(self, target_path: str) -> IngestResponse:
        path = Path(target_path)
        documents = discover_documents(path)
        root = path if path.is_dir() else path.parent
        chunks = build_chunks(
            documents,
            root=root,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        chunk_count = self.repository.upsert_chunks(chunks)
        return IngestResponse(files_indexed=len(documents), chunks_indexed=chunk_count)

    def search(self, question: str, top_k: int | None = None):
        rows = self.repository.list_chunks()
        return rank_chunks(question, rows, top_k=top_k or settings.default_top_k)

    def query(self, question: str, top_k: int | None = None) -> QueryResponse:
        ranked = self.search(question, top_k=top_k)
        answer = build_answer(question, ranked)
        citations = [
            Citation(
                chunk_id=chunk.chunk_id,
                source_path=chunk.source_path,
                score=chunk.score,
                snippet=chunk.content[:200],
            )
            for chunk in ranked
        ]
        return QueryResponse(question=question, answer=answer, citations=citations)

    def evaluate(self, dataset_path: str) -> EvaluationResponse:
        dataset = load_eval_dataset(Path(dataset_path))
        results = []
        for example in dataset:
            response = self.query(example["question"], top_k=example.get("top_k", settings.default_top_k))
            retrieved_sources = [citation.source_path for citation in response.citations]
            expected_sources = example.get("expected_sources", [])
            result = EvaluationExampleResult(
                question=example["question"],
                answer=response.answer,
                matched_expected_sources=sum(
                    1 for source in expected_sources if source in retrieved_sources
                ),
                expected_sources=expected_sources,
                retrieved_sources=retrieved_sources,
                grounded=grounded(response.answer, retrieved_sources, expected_sources),
            )
            results.append(result)
        return build_evaluation_response(results)
