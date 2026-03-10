# from langchain_core.tools import tool
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.infrastructure.db.vector_repository_impl import VectorRepositoryImpl


# @tool
# async def vector_search_tool(
#     query: str,
#     limit: int = 5,
#     session: AsyncSession = None,
# ) -> list[dict]:
#     """
#     Семантический поиск автомобильных объявлений по смыслу запроса.
#     Используй когда запрос описательный: 'надёжное авто для семьи', 'экономичный городской автомобиль'.

#     Args:
#         query: Текстовый запрос для поиска
#         limit: Количество результатов (по умолчанию 5)
#     """
#     repo = VectorRepositoryImpl(session=session)
#     return await repo.search_by_embedding(query=query, limit=limit)

from langchain_core.tools import tool
from src.infrastructure.db.vector_repository_impl import VectorRepositoryImpl
from src.infrastructure.db.session import async_session_factory


@tool
async def vector_search_tool(query: str, limit: int = 5) -> list[dict]:
    """
    Семантический поиск автомобильных объявлений по смыслу запроса.
    Используй когда запрос описательный: 'надёжное авто для семьи', 'экономичный городской автомобиль'.

    Args:
        query: Текстовый запрос для поиска
        limit: Количество результатов (по умолчанию 5)
    """
    async with async_session_factory() as session:
        repo = VectorRepositoryImpl(session=session)
        return await repo.search_by_embedding(query=query, limit=limit)