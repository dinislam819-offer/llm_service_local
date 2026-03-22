# src/infrastructure/llm/embeddings.py
from src.config.settings import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_ollama import OllamaEmbeddings


def get_embeddings(task_type: str = "retrieval_document"):
    """
    task_type="retrieval_document" — при ingestion (записываем документы)
    task_type="retrieval_query"    — при поиске (запрос пользователя)
    """
    if settings.embedding_provider in ("google", "google_genai"):
        return GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
            task_type=task_type,
        )

    if settings.embedding_provider == "huggingface":
        return FastEmbedEmbeddings(
            model_name=settings.embedding_model,
            cache_dir=settings.huggingface_cache_dir,
        )

    if settings.embedding_provider == "openai":
        return OpenAIEmbeddings(
            model=settings.embedding_model,
            dimensions=settings.embedding_dimensions,
            api_key=settings.openai_api_key,
        )

    # default: ollama
    return OllamaEmbeddings(
        model=settings.embedding_model,
        base_url=settings.ollama_base_url,
    )