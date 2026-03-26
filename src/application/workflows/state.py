# src/application/workflows/state.py
import operator
from typing import Annotated, List, Optional, TypedDict
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class ChatState(TypedDict):
    # ── Входные данные ──
    user_query: str
    chat_id: int | None

    # ── История сообщений ──
    messages: Annotated[list[BaseMessage], add_messages]

    # ── Результаты агентов ──
    is_relevant: bool
    moderation_reason: str
    intent: str

    # ── Новые поля для Query Agent / Reranker ──
    rewritten_query: str | None        # переписанный запрос
    reranked: bool                     # флаг, что уже ранжировали документы

    # РАЗДЕЛЁННЫЕ выходы параллельных агентов
    # Annotated[..., operator.add] — значения СКЛЕИВАЮТСЯ (list + list)
    rag_documents: Annotated[list[dict], operator.add]
    sql_documents: Annotated[list[dict], operator.add]

    # Финальный объединённый результат (заполняет aggregator)
    # retrieved_documents: Annotated[list[dict], operator.add]
    retrieved_documents: list[dict]

    # Если хотим собирать историю всех сгенерированных SQL-запросов:
    # sql_queries: Annotated[list[str], operator.add]
    # Annotated[..., last_value] — берётся последнее значение (от sql_agent)
    sql_query: str

    # ── Финальный ответ ──
    final_answer: str