# src/application/agents/rag_agent.py
from pydantic import BaseModel, Field
from src.infrastructure.llm.provider_factory import get_llm
from src.application.workflows.state import ChatState
from src.application.tools.vector_search import vector_search_tool
import logging

logger = logging.getLogger(__name__)

class SearchFilters(BaseModel):
    """Параметры фильтрации извлечённые из запроса пользователя."""
    query: str = Field(description="Очищенный поисковый запрос для векторного поиска")
    max_price: float | None = Field(default=None, description="Максимальная цена в рублях")
    min_price: float | None = Field(default=None, description="Минимальная цена в рублях")
    city: str | None = Field(default=None, description="Город")
    brand: str | None = Field(default=None, description="Марка автомобиля")
    min_year: int | None = Field(default=None, description="Год выпуска от")
    max_year: int | None = Field(default=None, description="Год выпуска до")


async def rag_agent_node(state: ChatState) -> dict:
    logger.warning("RAG AGENT NODE CALLED: query=%s", state["user_query"])

    llm = get_llm()
    structured_llm = llm.with_structured_output(SearchFilters)
    filters: SearchFilters = await structured_llm.ainvoke(
        f"Извлеки параметры поиска автомобиля из запроса: {state['user_query']}"
    )
    logger.warning("RAG AGENT filters: %s", filters)

    results = await vector_search_tool.ainvoke({
        "query": filters.query,
        "limit": 5,
        "max_price": filters.max_price,
        "min_price": filters.min_price,
        "city": filters.city,
        "brand": filters.brand,
        "min_year": filters.min_year,
        "max_year": filters.max_year,
    })

    logger.warning("RAG AGENT results count: %d", len(results))
    # return {"retrieved_documents": results or []}

    # Новая часть для параллельных агентов
    return {"rag_documents": results or []}