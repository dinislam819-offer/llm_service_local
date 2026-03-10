from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.db.models import Chat, ChatMessage


class ChatRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_chat(self, title: str | None = None) -> int:
        chat = Chat(title=title)
        self.session.add(chat)
        await self.session.commit()
        await self.session.refresh(chat)
        return chat.id

    async def save_message(self, chat_id: int, role: str, content: str) -> None:
        message = ChatMessage(chat_id=chat_id, role=role, content=content)
        self.session.add(message)
        await self.session.commit()

    async def get_history(self, chat_id: int) -> list[ChatMessage]:
        result = await self.session.execute(
            select(ChatMessage)
            .where(ChatMessage.chat_id == chat_id)
            .order_by(ChatMessage.created_at)
        )
        return result.scalars().all()