.PHONY: install test lint ingest-sample query serve evaluate

install:
	pip install -e .[dev]

test:
	python -m unittest discover -s tests -v

lint:
	ruff check src tests

ingest-sample:
	rag-platform ingest data/sample_corpus

query:
	rag-platform query "$(Q)"

serve:
	python -m rag_platform.main

evaluate:
	rag-platform evaluate data/eval/sample_eval.jsonl
