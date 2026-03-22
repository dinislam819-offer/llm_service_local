# src/application/dto/sql_query_dto.py
from pydantic import BaseModel, Field

class SQLQueryResult(BaseModel):
    """Structured output SQL-агента."""

    sql_query: str = Field(
        description="Готовый SQL SELECT запрос к таблице avito_listings"
    )
    explanation: str = Field(
        description="Краткое объяснение что ищет этот запрос"
    )