from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class ChatState(TypedDict):
    # ── Входные данные ──
    user_query: str                              # оригинальный запрос пользователя
    chat_id: int | None                          # ID чата для сохранения истории

    # ── История сообщений ──
    # add_messages — reducer: новые сообщения добавляются, не перезаписывают
    messages: Annotated[list[BaseMessage], add_messages]

    # ── Результаты агентов (промежуточные) ──
    is_relevant: bool                            # moderation agent
    moderation_reason: str                       # причина блокировки, если нерелевантно

    retrieved_documents: list[dict]              # rag agent: найденные вакансии
    sql_query: str                               # sql agent: сформированный запрос
    sql_results: list[dict]                      # sql agent: результаты из БД

    # ── Финальный ответ ──
    final_answer: str                            # writer agent