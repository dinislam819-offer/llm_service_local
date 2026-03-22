# src/infrastructure/llm/provider_factory.py
from langchain.chat_models import init_chat_model
from src.config.settings import settings


def get_llm():
    kwargs = {
        "model": settings.LLM_MODEL,
        "model_provider": settings.LLM_PROVIDER,
    }
    if settings.LLM_PROVIDER == "ollama":
        kwargs["base_url"] = settings.OLLAMA_BASE_URL
    return init_chat_model(**kwargs)