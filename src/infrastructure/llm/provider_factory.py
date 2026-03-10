# src/infrastructure/llm/provider_factory.py
from langchain.chat_models import init_chat_model
from src.config.settings import settings


def get_llm():
    kwargs = {
        "model": settings.llm_model,
        "model_provider": settings.llm_provider,
        "temperature": settings.llm_temperature,
    }
    if settings.llm_base_url:
        kwargs["base_url"] = settings.llm_base_url
    return init_chat_model(**kwargs)