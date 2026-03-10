from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    chat_id: int | None = None


class DocumentOut(BaseModel):
    id: int | None = None
    title: str | None = None
    company: str | None = None
    location: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    description: str | None = None
    score: float | None = None


class ChatResponse(BaseModel):
    chat_id: int
    answer: str
    documents: list[DocumentOut]
    is_relevant: bool