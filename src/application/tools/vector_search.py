# src/application/tools/vector_search.py
from langchain_core.tools import tool
from src.infrastructure.db.vector_repository_impl import VectorRepositoryImpl
from src.infrastructure.db.session import async_session_factory


@tool
async def vector_search_tool(
    query: str,
    limit: int = 5,
    max_price: float | None = None,
    min_price: float | None = None,
    city: str | None = None,
    brand: str | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
) -> list[dict]:
    """
    Поиск автомобильных объявлений на Авито по семантическому смыслу.
    Используй для ЛЮБОГО запроса связанного с поиском автомобилей.

    Args:
        query: Поисковый запрос (марка, модель, город, характеристики)
        limit: Количество результатов (по умолчанию 5)
        max_price: Максимальная цена в рублях
        min_price: Минимальная цена в рублях
        city: Город поиска
        brand: Марка автомобиля (Toyota, BMW, и т.д.)
    """
    async with async_session_factory() as session:
        repo = VectorRepositoryImpl(session=session)
        return await repo.search_by_embedding(
            query=query,
            limit=limit,
            max_price=max_price,
            min_price=min_price,
            city=city,
            brand=brand,
            min_year=min_year, 
            max_year=max_year,
        )