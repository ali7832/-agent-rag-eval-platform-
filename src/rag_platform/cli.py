import argparse
import json

from rag_platform.service import RagPlatformService


service = RagPlatformService()

def ingest(path: str) -> None:
    response = service.ingest(path)
    print(
        f"Indexed {response.files_indexed} files and {response.chunks_indexed} chunks from '{path}'."
    )


def search(question: str, top_k: int = 4) -> None:
    results = service.search(question, top_k=top_k)
    print("Search Results")
    for result in results:
        print(f"- {result.source_path} | {result.score} | {result.content[:120]}")


def query(question: str, top_k: int = 4) -> None:
    response = service.query(question, top_k=top_k)
    print(response.answer)
    print("")
    print("Citations:")
    for citation in response.citations:
        print(f"- {citation.source_path} ({citation.score})")


def evaluate(dataset_path: str) -> None:
    response = service.evaluate(dataset_path)
    print(json.dumps(response.model_dump(), indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Developer CLI for the Agent RAG Evaluation Platform.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("path")

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("question")
    search_parser.add_argument("--top-k", type=int, default=4)

    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("question")
    query_parser.add_argument("--top-k", type=int, default=4)

    evaluate_parser = subparsers.add_parser("evaluate")
    evaluate_parser.add_argument("dataset_path")

    args = parser.parse_args()

    if args.command == "ingest":
        ingest(args.path)
    elif args.command == "search":
        search(args.question, top_k=args.top_k)
    elif args.command == "query":
        query(args.question, top_k=args.top_k)
    elif args.command == "evaluate":
        evaluate(args.dataset_path)


if __name__ == "__main__":
    main()
