from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage

from src.application.dto.moderation_dto import ModerationResult
from src.application.workflows.state import ChatState
from src.infrastructure.llm.provider_factory import get_llm


# Загружаем промпт из файла
_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "moderation.txt"
_PROMPT_TEMPLATE = _PROMPT_PATH.read_text(encoding="utf-8")


def moderation_node(state: ChatState) -> dict:
    """
    Узел модерации: проверяет релевантность запроса.
    Возвращает обновление состояния графа.
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(ModerationResult)

    prompt = _PROMPT_TEMPLATE.format(user_query=state["user_query"])

    result: ModerationResult = structured_llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "is_relevant": result.is_relevant,
        "moderation_reason": result.reason,
        "messages": [
            HumanMessage(content=state["user_query"])
        ],
    }


def should_continue_after_moderation(state: ChatState) -> str:
    """
    Роутер после moderation_node.
    Определяет следующий узел графа.
    """
    if state["is_relevant"]:
        return "rag_agent"
    return "blocked"