from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src.application.workflows.state import ChatState
from src.application.agents.moderation_agent import (
    moderation_node,
    should_continue_after_moderation,
)
from src.application.agents.rag_agent import (
    rag_agent_node,
    rag_tool_node,
    should_continue_rag,
    collect_retrieved_documents,
)
from src.application.agents.writer_agent import blocked_node, writer_node  # writer добавим ниже


def build_chat_graph():
    graph = StateGraph(ChatState)

    # ── Узлы ──
    graph.add_node("moderation", moderation_node)
    graph.add_node("blocked", blocked_node)
    graph.add_node("rag_agent", rag_agent_node)
    graph.add_node("tools", rag_tool_node)          # ToolNode — отдельный узел
    graph.add_node("collect_docs", collect_retrieved_documents)
    graph.add_node("writer", writer_node)            # добавим в следующем шаге

    # ── Стартовая точка ──
    graph.set_entry_point("moderation")

    # ── Рёбра ──
    graph.add_conditional_edges(
        "moderation",
        should_continue_after_moderation,
        {
            "rag_agent": "rag_agent",
            "blocked": "blocked",
        },
    )

    # RAG-цикл: agent → tools → agent → ... → writer
    graph.add_conditional_edges(
        "rag_agent",
        should_continue_rag,
        {
            "tools": "tools",
            "writer": "collect_docs",
        },
    )
    graph.add_edge("tools", "rag_agent")           # после tools снова агент
    graph.add_edge("collect_docs", "writer")
    graph.add_edge("blocked", END)
    graph.add_edge("writer", END)

    return graph.compile()


chat_graph = build_chat_graph()