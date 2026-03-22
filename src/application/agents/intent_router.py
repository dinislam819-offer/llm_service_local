# src/application/agents/intent_router.py
import logging
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field
from src.application.workflows.state import ChatState
from src.infrastructure.llm.provider_factory import get_llm

logger = logging.getLogger(__name__)


class IntentResult(BaseModel):
    intent: str = Field(description="Тип запроса: sql или rag")
    reason: str = Field(description="Причина классификации")


_llm = get_llm()
_structured_llm = _llm.with_structured_output(IntentResult)

_ROUTER_PROMPT = """Определи тип поискового запроса об автомобиле.

Верни "sql" если запрос содержит точные фильтры: цена, город, год, пробег, марка, модель.
Верни "rag" если запрос описательный: надёжность, характеристики, советы, сравнения.

Примеры sql: "Toyota до 800к", "BMW в Москве 2020", "пробег до 50000"
Примеры rag: "надёжный семейный автомобиль", "что лучше Toyota или Kia"

Запрос: {user_query}"""


async def intent_router_node(state: ChatState) -> dict:
    prompt = _ROUTER_PROMPT.format(user_query=state["user_query"])
    result: IntentResult = await _structured_llm.ainvoke([
        HumanMessage(content=prompt)
    ])
    logger.warning("INTENT ROUTER: query='%s' → intent='%s' reason='%s'",
                   state["user_query"], result.intent, result.reason)
    return {"intent": result.intent}


def route_by_intent(state: ChatState) -> str:
    intent = state.get("intent", "rag")
    logger.warning("ROUTE BY INTENT: routing to '%s'", intent)
    return intent