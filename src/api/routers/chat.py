# src/api/routes/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_session
from src.api.schemas import ChatRequest, ChatResponse
from src.application.services.chat_service import ChatService

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
):
    service = ChatService(session=session)
    result = await service.process_message(
        message=request.message,
        chat_id=request.chat_id,
    )
    return ChatResponse(
        chat_id=result["chat_id"],
        answer=result["answer"],
        documents=result.get("documents", []),
        is_relevant=result["is_relevant"],
    )

@router.get("/chat/{chat_id}/history")
async def get_chat_history(
    chat_id: int,
    session: AsyncSession = Depends(get_session),
):
    from src.infrastructure.db.chat_repository_impl import ChatRepositoryImpl
    repo = ChatRepositoryImpl(session)
    messages = await repo.get_history(chat_id)
    return [
        {"role": m.role, "content": m.content, "created_at": m.created_at}
        for m in messages
    ]