import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from rag_platform.service import RagPlatformService

try:
    from fastapi import FastAPI

    from rag_platform.schemas import (
        EvaluationRequest,
        EvaluationResponse,
        HealthResponse,
        IngestRequest,
        IngestResponse,
        QueryRequest,
        QueryResponse,
    )
except ModuleNotFoundError:  # pragma: no cover - exercised only in offline environments.
    FastAPI = None


service = RagPlatformService()

if FastAPI is not None:
    app = FastAPI(title="Agent RAG Evaluation Platform", version="0.1.0")

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok")


    @app.post("/ingest", response_model=IngestResponse)
    def ingest(request: IngestRequest) -> IngestResponse:
        return service.ingest(request.path)


    @app.post("/query", response_model=QueryResponse)
    def query(request: QueryRequest) -> QueryResponse:
        return service.query(request.question, top_k=request.top_k)


    @app.post("/evaluate", response_model=EvaluationResponse)
    def evaluate(request: EvaluationRequest) -> EvaluationResponse:
        return service.evaluate(request.dataset_path)
else:
    app = None


class FallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/health":
            self.send_response(404)
            self.end_headers()
            return
        body = json.dumps({"status": "ok"}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return


def main() -> None:
    if app is not None:
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8000)
        return

    server = HTTPServer(("0.0.0.0", 8000), FallbackHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
