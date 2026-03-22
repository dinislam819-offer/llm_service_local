# src/application/agents/moderation_agent.py
from pathlib import Path
from langchain_core.messages import HumanMessage
from src.application.dto.moderation_dto import ModerationResult
from src.application.workflows.state import ChatState
from src.infrastructure.llm.provider_factory import get_llm

_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "moderation.txt"
_PROMPT_TEMPLATE = _PROMPT_PATH.read_text(encoding="utf-8")

# LLM создаётся один раз при старте, не при каждом запросе
_llm = get_llm()
_structured_llm = _llm.with_structured_output(ModerationResult)

async def moderation_node(state: ChatState) -> dict:  # async
    prompt = _PROMPT_TEMPLATE.format(user_query=state["user_query"])

    result: ModerationResult = await _structured_llm.ainvoke([  # ainvoke
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
    if state["is_relevant"]:
        return "rag_agent"
    return "blocked"