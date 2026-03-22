# src/api/routes/avto.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.deps import get_session

router = APIRouter()

@router.get("/avto")
async def list_avto(
    session: AsyncSession = Depends(get_session),
    limit: int = 20,
    offset: int = 0,
):
    # TODO: реализовать через avto_repository
    return {"avto": [], "total": 0}