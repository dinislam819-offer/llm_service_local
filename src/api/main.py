"""ASGI entrypoint for the LLM service."""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.db.session import create_db_and_tables, engine
from src.api.routers import chat, avto, health

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup и shutdown логика приложения."""
    logger.info("Starting up...")
    await create_db_and_tables()
    logger.info("Database tables created.")
    yield
    # Shutdown: закрываем пул соединений
    await engine.dispose()
    logger.info("Database connections closed.")


app = FastAPI(
    title="Avto Search Bot API",
    description="AI-powered avto search chatbot with RAG",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(avto.router, prefix="/api/v1", tags=["Avto"])