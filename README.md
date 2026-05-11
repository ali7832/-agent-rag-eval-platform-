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
- Docker, Kubernetes manifests, Makefile, and CI
- Testable, extensible Python package structure

## Architecture

```text
Documents -> Loaders -> Chunker -> Repository -> Retriever -> Generator -> Evaluator -> API/CLI
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
make test
make ingest-sample
make query Q="What is the platform designed to evaluate?"
make serve
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
```

## CLI examples

```bash
rag-platform ingest data/sample_corpus
rag-platform search "evaluation groundedness"
rag-platform query "How does ingestion work?"
rag-platform evaluate data/eval/sample_eval.jsonl
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

## Portfolio positioning

This project is intentionally designed to support senior AI/ML interviews. It gives concrete talking points around architecture, evaluation, latency, grounding, retrieval tradeoffs, testing, production deployment, and incremental improvement of LLM systems.
