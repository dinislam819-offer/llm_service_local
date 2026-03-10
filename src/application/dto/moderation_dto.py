from pydantic import BaseModel, Field


class ModerationResult(BaseModel):
    """Результат проверки релевантности запроса."""

    is_relevant: bool = Field(
        description="True если запрос относится к поиску вакансий или рынку труда"
    )
    reason: str = Field(
        description="Краткое объяснение решения (1-2 предложения)"
    )
    category: str = Field(
        description="Категория запроса: 'avto_search' | 'market_info' | 'off_topic' | 'inappropriate'"
    )