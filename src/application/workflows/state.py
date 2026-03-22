# src/application/workflows/state.py
import operator
from typing import Annotated, List, Optional, TypedDict
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# class ChatState(TypedDict):
#     # ── Входные данные ──
#     user_query: str
#     # retrieved_documents: List[dict]  # Общий список для гибрида
#     # sql_documents: List[dict]        # Только SQL результаты
#     # vector_documents: List[dict]     # Только векторные
#     chat_id: int | None

#     # ── История сообщений ──
#     messages: Annotated[list[BaseMessage], add_messages]

#     # ── Результаты агентов ──
#     is_relevant: bool
#     moderation_reason: str
#     intent: str                                  # "rag" | "sql"

#     retrieved_documents: Annotated[list[dict], operator.add]  # накопление
#     sql_query: str                               # для логирования/дебага

#     # ── Финальный ответ ──
#     final_answer: str


# Это новая часть для параллельных агентов
class ChatState(TypedDict):
    # ── Входные данные ──
    user_query: str
    chat_id: int | None

    # ── История сообщений ──
    messages: Annotated[list[BaseMessage], add_messages]

    # ── Результаты агентов ──
    is_relevant: bool
    moderation_reason: str
    intent: str                         # можно оставить, но он уже не критичен

    # РАЗДЕЛЕННЫЕ выходы агентов
    rag_documents: list[dict]
    sql_documents: list[dict]

    # Финальный объединённый результат (заполняет aggregator)
    retrieved_documents: list[dict]

    sql_query: str                      # можно оставить

    # ── Финальный ответ ──
    final_answer: str