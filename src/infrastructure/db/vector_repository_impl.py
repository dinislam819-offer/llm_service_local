from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.db.models import AvitoListing
from src.infrastructure.llm.embeddings import get_embeddings


class VectorRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.embeddings = get_embeddings()

    async def search_by_embedding(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:
        """
        Поиск объявлений по косинусному сходству.
        Возвращает топ-N наиболее релевантных объявлений.
        """
        # Генерируем вектор запроса
        query_vector = await self.embeddings.aembed_query(query)

        # Косинусное расстояние: чем меньше — тем похожее
        distance_col = AvitoListing.embedding.cosine_distance(query_vector)

        statement = (
            select(AvitoListing, distance_col.label("distance"))
            .order_by(distance_col)
            .limit(limit)
        )

        result = await self.session.execute(statement)
        rows = result.all()

        return [
            {
                "id": listing.id,
                "item_id": listing.item_id,
                "title": listing.title,
                "description": listing.description[:400],
                "price": listing.price,
                "city": listing.city,
                "category_name": listing.category_name,
                "param_1": listing.param_1,
                "param_2": listing.param_2,
                "score": round(1 - distance, 4),  # сходство 0..1
            }
            for listing, distance in rows
        ]