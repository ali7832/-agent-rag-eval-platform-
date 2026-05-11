import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List

from rag_platform.chunking import Chunk


class SQLiteChunkRepository:
    def __init__(self, database_path: Path):
        self.database_path = database_path
        self._initialize()

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self.connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    source_path TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    content TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def upsert_chunks(self, chunks: List[Chunk]) -> int:
        with self.connection() as connection:
            connection.executemany(
                """
                INSERT INTO chunks (chunk_id, source_path, position, content)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(chunk_id) DO UPDATE SET
                    source_path = excluded.source_path,
                    position = excluded.position,
                    content = excluded.content
                """,
                [(chunk.chunk_id, chunk.source_path, chunk.position, chunk.content) for chunk in chunks],
            )
            connection.commit()
        return len(chunks)

    def list_chunks(self) -> List[sqlite3.Row]:
        with self.connection() as connection:
            rows = connection.execute(
                "SELECT chunk_id, source_path, position, content FROM chunks ORDER BY source_path, position"
            ).fetchall()
        return list(rows)
