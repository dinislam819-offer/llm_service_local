# src/application/agents/writer_agent.py
import json
from pathlib import Path
from langchain_core.messages import AIMessage, HumanMessage
from src.application.dto.writer_dto import WriterResult
from src.application.workflows.state import ChatState
from src.infrastructure.llm.provider_factory import get_llm

_PROMPT_TEMPLATE = (
    Path(__file__).parent.parent.parent / "prompts" / "writer.txt"
).read_text(encoding="utf-8")

# LLM создаётся один раз при старте
_llm = get_llm()
_structured_llm = _llm.with_structured_output(WriterResult)

def _format_documents(documents: list[dict]) -> str:
    """Форматирует найденные автомобили в читаемый текст для промпта."""
    if not documents:
        return "Автомобили не найдены."

    lines = []
    for i, doc in enumerate(documents, 1):
        # Цена
        price = doc.get("price")
        price_str = f"{price:,} ₽".replace(",", " ") if price else "цена не указана"

        # Пробег
        mileage = doc.get("mileage")
        mileage_str = f"{mileage:,} км".replace(",", " ") if mileage else "пробег не указан"

        lines.append(
            f"{i}. {doc.get('brand', '?')} {doc.get('model', '')} "
            f"{doc.get('year', '')}г.\n"
            f"   {price_str} | {mileage_str}\n"
            f"   {doc.get('engine', '')} | {doc.get('transmission', '')}\n"
            f"   {doc.get('location', 'не указан')}\n"
            f"   {doc.get('description', '')[:200]}"
        )
    return "\n\n".join(lines)

async def writer_node(state: ChatState) -> dict:  # async
    documents = state.get("retrieved_documents", [])
    formatted_docs = _format_documents(documents)

    prompt = _PROMPT_TEMPLATE.format(
        user_query=state["user_query"],
        documents=formatted_docs,
    )

    result: WriterResult = await _structured_llm.ainvoke([  # ainvoke
        HumanMessage(content=prompt)
    ])

    ai_message = AIMessage(content=result.answer)

    return {
        "final_answer": result.answer,
        "messages": [ai_message],
    }

def blocked_node(state: ChatState) -> dict:
    """Узел для нерелевантных запросов."""
    message = (
        f"Извините, ваш запрос не относится к поиску автомобилей. "
        f"Причина: {state.get('moderation_reason', 'запрос нерелевантен')}. "
        f"Я могу помочь найти автомобиль, узнать о ценах или характеристиках."
    )
    return {
        "final_answer": message,
        "messages": [AIMessage(content=message)],
    }