import unittest
from pathlib import Path

from rag_platform.service import RagPlatformService
from rag_platform.storage import SQLiteChunkRepository


class IngestionTests(unittest.TestCase):
    def test_ingest_indexes_sample_corpus(self) -> None:
        tmp_path = Path("test_ingestion.db")
        repository = SQLiteChunkRepository(tmp_path)
        service = RagPlatformService(repository=repository)

        response = service.ingest("data/sample_corpus")

        self.assertGreaterEqual(response.files_indexed, 3)
        self.assertGreaterEqual(response.chunks_indexed, response.files_indexed)
        self.assertTrue(repository.list_chunks())
        if tmp_path.exists():
            tmp_path.unlink()
