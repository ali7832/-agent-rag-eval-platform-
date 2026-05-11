import unittest
from pathlib import Path

from rag_platform.service import RagPlatformService
from rag_platform.storage import SQLiteChunkRepository


class EvaluationTests(unittest.TestCase):
    def test_evaluation_reports_hit_rate(self) -> None:
        database_path = Path("test_eval.db")
        repository = SQLiteChunkRepository(database_path)
        service = RagPlatformService(repository=repository)
        service.ingest("data/sample_corpus")

        response = service.evaluate("data/eval/sample_eval.jsonl")

        self.assertEqual(response.examples, 3)
        self.assertGreater(response.retrieval_hit_rate, 0)
        self.assertGreater(response.grounded_rate, 0)
        if database_path.exists():
            database_path.unlink()
