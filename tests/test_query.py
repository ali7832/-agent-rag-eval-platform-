import unittest
from pathlib import Path

from rag_platform.service import RagPlatformService
from rag_platform.storage import SQLiteChunkRepository


class QueryTests(unittest.TestCase):
    def test_query_returns_grounded_citations(self) -> None:
        database_path = Path("test_query.db")
        repository = SQLiteChunkRepository(database_path)
        service = RagPlatformService(repository=repository)
        service.ingest("data/sample_corpus")

        response = service.query("What does the platform evaluate?", top_k=3)

        self.assertIn("indexed corpus", response.answer)
        self.assertTrue(response.citations)
        self.assertTrue(
            any(
                "evaluation" in citation.source_path or "architecture" in citation.source_path
                for citation in response.citations
            )
        )
        if database_path.exists():
            database_path.unlink()
