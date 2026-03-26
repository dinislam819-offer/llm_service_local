# src/application/agents/sql_agent.py
import logging
from pathlib import Path
from langchain_core.messages import HumanMessage
from src.application.dto.sql_query_dto import SQLQueryResult
from src.application.workflows.state import ChatState
from src.infrastructure.llm.provider_factory import get_llm
from src.application.tools.sql_search_tool import sql_search_tool

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE = (
    Path(__file__).parent.parent.parent / "prompts" / "sql_agent.txt"
).read_text(encoding="utf-8")

_llm = get_llm()
_structured_llm = _llm.with_structured_output(SQLQueryResult)

async def sql_agent_node(state: ChatState) -> dict:
    prompt = _PROMPT_TEMPLATE.format(user_query=state["user_query"])

    result: SQLQueryResult = await _structured_llm.ainvoke([
        HumanMessage(content=prompt)
    ])

    # Логируем что сгенерировал LLM
    logger.warning("SQL AGENT generated query: %s", result.sql_query)
    logger.warning("SQL AGENT explanation: %s", result.explanation)

    sql_results = await sql_search_tool.ainvoke({"query": result.sql_query})

    # Логируем результат
    logger.warning("SQL AGENT results count: %d", len(sql_results))
    if sql_results:
        logger.warning("SQL AGENT first result: %s", sql_results[0])
    else:
        logger.warning("SQL AGENT no results returned")

    # Новая часть для параллельных агентов
    return {
    "sql_documents": sql_results or [],
    "sql_query": result.sql_query,
    }