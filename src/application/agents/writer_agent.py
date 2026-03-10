import json
from pathlib import Path
from langchain_core.messages import AIMessage, HumanMessage

from src.application.dto.writer_dto import WriterResult
from src.application.workflows.state import ChatState
from src.infrastructure.llm.provider_factory import get_llm

_PROMPT_TEMPLATE = (
    Path(__file__).parent.parent.parent / "prompts" / "writer.txt"
).read_text(encoding="utf-8")


def _format_documents(documents: list[dict]) -> str:
    """Форматирует найденные документы в читаемый текст для промпта."""
    if not documents:
        return "Вакансии не найдены."

    lines = []
    for i, doc in enumerate(documents, 1):
        salary = ""
        if doc.get("salary_min") and doc.get("salary_max"):
            currency = doc.get("salary_currency", "RUB")
            salary = f"{doc['salary_min']}–{doc['salary_max']} {currency}"
        elif doc.get("salary_min"):
            salary = f"от {doc['salary_min']} {doc.get('salary_currency', 'RUB')}"
        else:
            salary = "зарплата не указана"

        lines.append(
            f"{i}. {doc.get('title', 'Без названия')} — {doc.get('company', '?')}\n"
            f"   📍 {doc.get('location', 'не указана')} | 💰 {salary}\n"
            f"   {doc.get('description', '')[:200]}..."
        )
    return "\n\n".join(lines)


def writer_node(state: ChatState) -> dict:
    """
    Финальный узел: формирует ответ пользователю
    на основе найденных документов.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(WriterResult)

    documents = state.get("retrieved_documents", [])
    formatted_docs = _format_documents(documents)

    prompt = _PROMPT_TEMPLATE.format(
        user_query=state["user_query"],
        documents=formatted_docs,
    )

    result: WriterResult = structured_llm.invoke([
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
        f"Извините, ваш запрос не относится к поиску вакансий. "
        f"Причина: {state.get('moderation_reason', 'запрос нерелевантен')}. "
        f"Я могу помочь найти вакансии, узнать о зарплатах или требованиях работодателей."
    )
    return {
        "final_answer": message,
        "messages": [AIMessage(content=message)],
    }