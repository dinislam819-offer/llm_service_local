# src/api/routes/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.api.deps import get_session

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/health/db")
async def db_health_check(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"status": "ok", "db": result.scalar() == 1}