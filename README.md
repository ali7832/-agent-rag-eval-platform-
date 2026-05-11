# Agent RAG Evaluation Platform

Production-minded Retrieval-Augmented Generation platform for document ingestion, retrieval, answer generation, and quality evaluation.

This repository is built as a portfolio-grade AI engineering project: clean architecture, HTTP API, CLI workflows, SQLite persistence, Docker deployment, CI, tests, sample corpus, and evaluation harness.

## What it demonstrates

- FastAPI service design for AI systems
- Document ingestion, chunking, metadata extraction, and indexing
- Retrieval pipeline with lexical scoring and citation metadata
- Grounded answer generation with source references
- Offline evaluation for retrieval and answer quality
- SQLite persistence for local deployability
- Docker, CI, and developer tooling
- Testable, extensible Python package structure

## Architecture

```text
Documents -> Loaders -> Chunker -> Repository -> Retriever -> Generator -> Evaluator -> API/CLI
```

## Features

- Recursive ingestion over Markdown and text files
- Chunk-level SQLite persistence with deterministic chunk IDs
- Lexical retrieval with simple overlap-based ranking and source citations
- Citation-aware answer composition for explainable outputs
- Offline evaluation harness for retrieval hit rate and groundedness
- FastAPI endpoints for ingestion, querying, evaluation, and inspection
- Typer CLI for local workflows and interview demos

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
make test
python -m rag_platform.cli ingest data/sample_corpus
python -m rag_platform.cli query "What is the platform designed to evaluate?"
python -m rag_platform.main
```

Then open:

```text
http://localhost:8000/docs
```

## API examples

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/ingest -H 'Content-Type: application/json' -d '{"path":"data/sample_corpus"}'
curl -X POST http://localhost:8000/query -H 'Content-Type: application/json' -d '{"question":"What does the platform evaluate?","top_k":4}'
curl -X POST http://localhost:8000/evaluate -H 'Content-Type: application/json' -d '{"dataset_path":"data/eval/sample_eval.jsonl"}'
```

## CLI examples

```bash
python -m rag_platform.cli ingest data/sample_corpus
python -m rag_platform.cli search "evaluation groundedness"
python -m rag_platform.cli query "How does ingestion work?"
python -m rag_platform.cli evaluate data/eval/sample_eval.jsonl
```

## Repository layout

```text
src/rag_platform/
  chunking.py       Text chunking strategy
  generation.py     Citation-backed answer synthesis
  ingestion.py      File loading and indexing
  retrieval.py      Ranking and retrieval
  service.py        Application orchestration
  storage.py        SQLite persistence layer
  evaluation.py     Offline scoring harness
  main.py           FastAPI app with offline fallback
  cli.py            Local developer CLI
```

## Roadmap

- [x] Local ingestion pipeline
- [x] SQLite persistence
- [x] Citation-backed retrieval and generation
- [x] Offline evaluation harness
- [x] API and CLI
- [x] Docker and CI scaffolding
- [ ] Dense embeddings provider
- [ ] Hybrid retrieval + reranking
- [ ] LangGraph agent orchestration
- [ ] OpenTelemetry tracing
- [ ] Auth and multi-tenant workspaces

## Interview positioning

This project is intentionally designed to support senior AI/ML interviews. It gives concrete talking points around architecture, evaluation, latency, grounding, retrieval tradeoffs, testing, production deployment, and incremental improvement of LLM systems.
