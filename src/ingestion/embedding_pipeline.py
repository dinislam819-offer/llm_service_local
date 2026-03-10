import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models import AvitoListing
from src.infrastructure.llm.embeddings import get_embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class EmbeddingPipeline:
    def __init__(self):
        self.embeddings = get_embeddings()

    def _build_text(self, row: pd.Series) -> str:
        """
        Склеиваем title + description для эмбеддинга.
        Чем больше текста — тем точнее векторный поиск.
        """
        parts = [str(row.get("title", ""))]
        if row.get("description"):
            parts.append(str(row["description"])[:1000])
        if row.get("param_1"):
            parts.append(str(row["param_1"]))
        if row.get("param_2"):
            parts.append(str(row["param_2"]))
        return " | ".join(filter(None, parts))

    async def process_batch(
        self,
        batch: pd.DataFrame,
        session: AsyncSession,
    ) -> None:
        # Собираем тексты для батчевой генерации эмбеддингов
        texts = [self._build_text(row) for _, row in batch.iterrows()]

        # Батчевый вызов — намного быстрее чем по одному
        vectors = await self.embeddings.aembed_documents(texts)

        for (_, row), vector in zip(batch.iterrows(), vectors):
            listing = AvitoListing(
                item_id=str(row.get("item_id", "")),
                title=str(row.get("title", ""))[:500],
                description=str(row.get("description", ""))[:5000],
                price=float(row["price"]) if pd.notna(row.get("price")) else None,
                city=str(row["city"]) if pd.notna(row.get("city")) else None,
                category_name=str(row["category_name"]) if pd.notna(row.get("category_name")) else None,
                param_1=str(row["param_1"]) if pd.notna(row.get("param_1")) else None,
                param_2=str(row["param_2"]) if pd.notna(row.get("param_2")) else None,
                param_3=str(row["param_3"]) if pd.notna(row.get("param_3")) else None,
                embedding=vector,
            )
            session.add(listing)