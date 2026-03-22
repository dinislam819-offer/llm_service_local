# src/api/schemas.py
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    chat_id: int | None = None

class DocumentOut(BaseModel):
    id: int | None = None
    title: str | None = None
    description: str | None = None
    price: float | None = None
    year: int | None = None
    city: str | None = None
    brand: str | None = None
    model: str | None = None
    score: float | None = None

class ChatResponse(BaseModel):
    chat_id: int
    answer: str
    documents: list[DocumentOut]
    is_relevant: bool