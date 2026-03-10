from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode

from src.application.workflows.state import ChatState
from src.infrastructure.llm.provider_factory import get_llm
from src.application.tools.vector_search import vector_search_tool
from src.application.tools.sql_search_tool import sql_search_tool

_PROMPT_TEMPLATE = (
    Path(__file__).parent.parent.parent / "prompts" / "rag.txt"
).read_text(encoding="utf-8")

# Список инструментов, доступных RAG-агенту
RAG_TOOLS = [vector_search_tool, sql_search_tool]

# Готовый ToolNode для графа
rag_tool_node = ToolNode(RAG_TOOLS)


def rag_agent_node(state: ChatState) -> dict:
    """
    RAG-агент: ReAct-паттерн.
    LLM сам решает когда вызывать инструменты.
    """
    llm = get_llm()
    llm_with_tools = llm.bind_tools(RAG_TOOLS)

    system_prompt = _PROMPT_TEMPLATE.format(user_query=state["user_query"])

    response = llm_with_tools.invoke([
        SystemMessage(content=system_prompt),
        *state["messages"],
    ])

    return {"messages": [response]}


def should_continue_rag(state: ChatState) -> str:
    """
    Роутер внутри RAG-цикла.
    Если LLM вызвал tool — идём в tool_node.
    Если нет — переходим к writer.
    """
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "writer"


def collect_retrieved_documents(state: ChatState) -> dict:
    """
    После завершения RAG-цикла собираем все найденные документы
    из ToolMessage-ов в состояние.
    """
    import json
    from langchain_core.messages import ToolMessage

    documents = []
    for msg in state["messages"]:
        if isinstance(msg, ToolMessage):
            try:
                data = json.loads(msg.content)
                if isinstance(data, list):
                    documents.extend(data)
            except (json.JSONDecodeError, TypeError):
                pass

    return {"retrieved_documents": documents}