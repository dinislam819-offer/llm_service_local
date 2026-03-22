import asyncio
from src.core.llm import get_llm
# from src.core.config import settings
from src.config.settings import settings 


async def test():
    llm = get_llm()
    print(f"🚀 Используется: {settings.LLM_PROVIDER} - {settings.LLM_MODEL}")
    
    response = await llm.ainvoke("Привет! Ты готова работать с LangGraph?")
    print(f"✅ Ответ: {response.content}")

asyncio.run(test())