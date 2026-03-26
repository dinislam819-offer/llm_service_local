# src/core/llm.py
from langchain_ollama import ChatOllama
from src.config.settings import settings 

def get_llm():
    """Фабрика для создания LLM по конфигурации"""

    if settings.LLM_PROVIDER.lower() == "ollama":
        return ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.1
        )
    else:
        raise ValueError(f"Неизвестный провайдер: {settings.LLM_PROVIDER}")