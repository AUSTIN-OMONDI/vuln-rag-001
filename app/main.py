"""FastAPI wrapper exposing the vulnerable RAG over HTTP."""

from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import answer, KNOWLEDGE_BASE

app = FastAPI(title="vuln-rag-001")


class ChatRequest(BaseModel):
    message: str


class PoisonRequest(BaseModel):
    keyword: str
    content: str


@app.get("/")
def health():
    return {"status": "ok", "service": "vuln-rag-001"}


@app.post("/chat")
def chat(req: ChatRequest):
    return {"response": answer(req.message)}


@app.post("/poison")
def poison(req: PoisonRequest):
    """VULNERABILITY (unauthenticated KB write): plant a doc in the corpus."""
    KNOWLEDGE_BASE[req.keyword.lower()] = req.content
    return {"status": "poisoned", "keyword": req.keyword}
