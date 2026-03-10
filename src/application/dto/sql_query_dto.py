from pydantic import BaseModel, Field


class SQLQueryResult(BaseModel):
    """Structured output SQL-агента."""

    sql_query: str = Field(
        description="Готовый SQL SELECT запрос к таблице avto_postings"
    )
    explanation: str = Field(
        description="Краткое объяснение что ищет этот запрос"
    )