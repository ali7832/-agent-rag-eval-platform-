from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Agent RAG Evaluation Platform")


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query")
def query(request: QueryRequest) -> dict:
    return {
        "question": request.question,
        "answer": "This is a grounded placeholder response from the RAG platform.",
        "citations": [
            {
                "document": "sample_doc.md",
                "score": 0.98,
            }
        ],
    }
