# src/application/dto/moderation_dto.py
from pydantic import BaseModel, Field

class ModerationResult(BaseModel):
    """Результат проверки релевантности запроса."""

    is_relevant: bool = Field(
        description="True если запрос относится к поиску автомобилей или авторынку"
    )
    reason: str = Field(
        description="Краткое объяснение решения (1-2 предложения)"
    )
    category: str = Field(
        description="Категория запроса: 'auto_search' | 'market_info' | 'off_topic' | 'inappropriate'"
    )