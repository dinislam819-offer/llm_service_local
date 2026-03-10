from pathlib import Path
from langchain_core.messages import HumanMessage

from src.application.dto.sql_query_dto import SQLQueryResult
from src.application.workflows.state import ChatState
from src.infrastructure.llm.provider_factory import get_llm

_PROMPT_TEMPLATE = (
    Path(__file__).parent.parent.parent / "prompts" / "sql_agent.txt"
).read_text(encoding="utf-8")


async def sql_agent_node(state: ChatState, session) -> dict:
    """
    Узел SQL-агента: формирует SQL-запрос и выполняет его.
    """
    from src.application.tools.sql_search_tool import sql_search_tool

    llm = get_llm()
    structured_llm = llm.with_structured_output(SQLQueryResult)

    prompt = _PROMPT_TEMPLATE.format(user_query=state["user_query"])
    result: SQLQueryResult = await structured_llm.ainvoke([
        HumanMessage(content=prompt)
    ])

    # Выполняем сформированный запрос
    sql_results = await sql_search_tool.ainvoke({
        "query": result.sql_query,
        "session": session,
    })

    return {
        "sql_query": result.sql_query,
        "sql_results": sql_results,
    }