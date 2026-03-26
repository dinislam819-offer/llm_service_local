# src/application/agents/query_agent.py
from langchain_core.messages import HumanMessage
from src.core.llm import get_llm
from src.application.workflows.state import ChatState

import logging

logger = logging.getLogger(__name__)

_llm = get_llm()

_QUERY_REWRITE_PROMPT = """Ты — агент переформулировки запросов для поиска.
Верни одну строку — уточнённый, максимально информативный запрос на русском,
без лишних пояснений.

Оригинальный запрос:
{query}
"""

async def query_agent_node(state: ChatState) -> ChatState:
    """Переформулирует пользовательский запрос для лучшего поиска."""
    user_message = state["messages"][-1].content
    prompt = _QUERY_REWRITE_PROMPT.format(query=user_message)
    resp = await _llm.ainvoke([HumanMessage(content=prompt)])
    state["rewritten_query"] = resp.content.strip()
    return state