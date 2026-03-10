from pydantic import BaseModel, Field


class WriterResult(BaseModel):
    """Structured output writer-агента."""

    answer: str = Field(
        description="Итоговый ответ пользователю на русском языке"
    )
    total_found: int = Field(
        description="Количество найденных вакансий"
    )
    has_results: bool = Field(
        description="True если найдены релевантные вакансии"
    )