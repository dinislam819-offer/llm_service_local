# src/application/services/chat_service.py 
from sqlalchemy.ext.asyncio import AsyncSession
from langchain_core.messages import HumanMessage
from src.application.workflows.chat_graph import chat_graph
from src.infrastructure.db.chat_repository_impl import ChatRepositoryImpl

class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.chat_repo = ChatRepositoryImpl(session)

    async def process_message(
        self,
        message: str,
        chat_id: int | None = None,
    ) -> dict:
        """
        Обрабатывает сообщение пользователя через LangGraph граф.
        Возвращает ответ и найденные документы.
        """
        # Создаём новый чат если не передан
        if chat_id is None:
            chat_id = await self.chat_repo.create_chat(title=message[:50])

        # Сохраняем сообщение пользователя
        await self.chat_repo.save_message(
            chat_id=chat_id,
            role="user",
            content=message,
        )

        # Начальное состояние графа
        initial_state = {
            "user_query": message,
            "chat_id": chat_id,
            "messages": [HumanMessage(content=message)],
            "is_relevant": False,
            "moderation_reason": "",
            "retrieved_documents": [],
            # "sql_query": "",
            # "sql_results": [],
            "final_answer": "",
        }

        # Запускаем граф
        result = await chat_graph.ainvoke(initial_state)

        final_answer = result.get("final_answer", "Не удалось сформировать ответ.")
        documents = result.get("retrieved_documents", [])

        # Сохраняем ответ ассистента
        await self.chat_repo.save_message(
            chat_id=chat_id,
            role="assistant",
            content=final_answer,
        )

        return {
            "chat_id": chat_id,
            "answer": final_answer,
            "documents": documents,
            "is_relevant": result.get("is_relevant", False),
        }