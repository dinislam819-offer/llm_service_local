from collections.abc import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.session import async_session_factory
from src.infrastructure.llm.provider_factory import get_llm

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

def get_chat_llm():
    return get_llm()