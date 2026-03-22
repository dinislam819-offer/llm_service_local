# src/infrastructure/db/vector_repository_impl.py
from sqlalchemy import and_
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
        max_price: float | None = None,
        min_price: float | None = None,
        city: str | None = None,
        brand: str | None = None,
        min_year: int | None = None,
        max_year: int | None = None,
    ) -> list[dict]:
        query_vector = await self.embeddings.aembed_query(query)
        distance_col = AvitoListing.embedding.cosine_distance(query_vector)

        # Собираем SQL-фильтры
        filters = []
        if max_price is not None:
            filters.append(AvitoListing.price <= max_price)
        if min_price is not None:
            filters.append(AvitoListing.price >= min_price)
        if city is not None:
            filters.append(AvitoListing.city.ilike(f"%{city}%"))
        if brand is not None:
            filters.append(AvitoListing.param_1.ilike(f"%{brand}%"))
        if min_year is not None:
            filters.append(AvitoListing.year >= min_year)
        if max_year is not None:
            filters.append(AvitoListing.year <= max_year)

        statement = (
            select(AvitoListing, distance_col.label("distance"))
            .where(and_(*filters)) if filters else
            select(AvitoListing, distance_col.label("distance"))
        ).order_by(distance_col).limit(limit)

        result = await self.session.execute(statement)
        rows = result.all()

        return [
            {
                "id": listing.id,
                "item_id": listing.item_id,
                "title": listing.title,
                "description": listing.description[:400],
                "price": listing.price,
                "year": listing.year,       
                "city": listing.city,
                "brand": listing.param_2,    
                "model": listing.param_3,    
                "score": round(1 - distance, 4),
            }
            for listing, distance in rows
        ]