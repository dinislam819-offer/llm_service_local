from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import DateTime, Text, text
from pgvector.sqlalchemy import Vector

from src.config.settings import settings


class AvitoListing(SQLModel, table=True):
    __tablename__ = "avito_listings"

    id: int | None = Field(default=None, primary_key=True)

    # Основные поля из датасета
    item_id: str = Field(index=True)           # оригинальный ID из Авито
    title: str                                  # заголовок: "Toyota Camry 2018"
    description: str = Field(sa_column=Column(Text))
    price: float | None = None
    city: str | None = None
    category_name: str | None = None           # "Автомобили"
    param_1: str | None = None                 # марка: "Toyota"
    param_2: str | None = None                 # модель: "Camry"
    param_3: str | None = None                 # доп. параметр

    # Служебные поля
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=text("now()"))
    )

    # Вектор для семантического поиска
    embedding: list[float] = Field(
        sa_column=Column(Vector(settings.embedding_dimensions))
    )


# class ScrappedListing(SQLModel, table=True):
#     """Сырые данные до обработки."""
#     __tablename__ = "scrapped_listings"

#     id: int | None = Field(default=None, primary_key=True)
#     raw_str = Field(sa_column=Column(Text))  # JSON строка
#     source: str = "avito"
#     is_processed: bool = Field(default=False)
#     created_at: datetime = Field(
#         sa_column=Column(DateTime(timezone=True), server_default=text("now()"))
#     )

class ScrappedListing(SQLModel, table=True):
    """Сырые данные до обработки."""
    __tablename__ = "scrapped_listings"

    id: int | None = Field(default=None, primary_key=True)
    raw_str: str | None = Field(default=None, sa_column=Column(Text))  # JSON строка
    # raw_str = Field(sa_column=Column(Text))  # JSON строка
    # raw_str: str | None = Field(default=None)
    source: str = "avito"
    is_processed: bool = Field(default=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=text("now()"))
    )


# ── Чат ──

class Chat(SQLModel, table=True):
    __tablename__ = "chats"

    id: int | None = Field(default=None, primary_key=True)
    title: str | None = None
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=text("now()"))
    )


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"

    id: int | None = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chats.id")
    role: str                        # "user" | "assistant"
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), server_default=text("now()"))
    )