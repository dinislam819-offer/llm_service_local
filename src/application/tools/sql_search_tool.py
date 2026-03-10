# from langchain_core.tools import tool
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import text


# @tool
# async def sql_search_tool(
#     query: str,
#     session: AsyncSession = None,
# ) -> list[dict]:
#     """
#     Поиск вакансий через SQL-запрос по точным критериям.
#     Используй для фильтрации по зарплате, локации, опыту, специализации.

#     Args:
#         query: SQL SELECT запрос к таблице avto_postings
#     """
#     # Защита: разрешаем только SELECT
#     clean = query.strip().upper()
#     if not clean.startswith("SELECT"):
#         return [{"error": "Разрешены только SELECT запросы"}]

#     try:
#         result = await session.execute(text(query))
#         rows = result.mappings().all()
#         return [dict(row) for row in rows[:20]]  # максимум 20 строк
#     except Exception as e:
#         return [{"error": str(e)}]

from langchain_core.tools import tool
from sqlalchemy import text
from src.infrastructure.db.session import async_session_factory


@tool
async def sql_search_tool(query: str) -> list[dict]:
    """
    Поиск через SQL по точным критериям: цена, город, марка.

    Args:
        query: SQL SELECT запрос к таблице avito_listings
    """
    clean = query.strip().upper()
    if not clean.startswith("SELECT"):
        return [{"error": "Разрешены только SELECT запросы"}]

    try:
        async with async_session_factory() as session:
            result = await session.execute(text(query))
            rows = result.mappings().all()
            return [dict(row) for row in rows[:20]]
    except Exception as e:
        return [{"error": str(e)}]