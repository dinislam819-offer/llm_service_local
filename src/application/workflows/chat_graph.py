# src/application/workflows/chat_graph.py
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src.application.workflows.state import ChatState
from src.application.agents.moderation_agent import (
    moderation_node,
    should_continue_after_moderation,
)
from src.application.agents.intent_router import (
    intent_router_node,
    route_by_intent,
)
from src.application.agents.rag_agent import (
    rag_agent_node,
    # should_continue_rag,
    # collect_retrieved_documents,
)
from src.application.agents.sql_agent import sql_agent_node
from src.application.agents.writer_agent import blocked_node, writer_node

from src.application.agents.aggregator_agent import aggregator_node             # аггрегация полученных ответов

from src.application.agents.query_agent import query_agent_node                 # Новые агенты
from src.application.agents.reranker_agent import reranker_node                 # Новые агенты

import logging
logger = logging.getLogger(__name__)

def route_after_sql(state: ChatState) -> str:
    """Фоллбэк на RAG если SQL вернул пустой результат."""
    results = state.get("retrieved_documents") or []
    logger.warning("ROUTE AFTER SQL: retrieved_documents count = %d", len(results))
    if results:
        return "writer"
    return "rag_agent"

def build_chat_graph():
    graph = StateGraph(ChatState)

    # ── Узлы ──
    graph.add_node("moderation", moderation_node)
    graph.add_node("blocked", blocked_node)
    graph.add_node("intent_router", intent_router_node)

    # Новый узел переформулировки запроса
    graph.add_node("query_agent", query_agent_node)

    graph.add_node("rag_agent", rag_agent_node)
    graph.add_node("sql_agent", sql_agent_node)

    # Узел агрегации и переранжирования
    graph.add_node("aggregator", aggregator_node)
    graph.add_node("reranker", reranker_node)

    graph.add_node("writer", writer_node)

    # ── Стартовая точка ──
    graph.set_entry_point("moderation")

    # ── Рёбра ──
    graph.add_conditional_edges(
        "moderation",
        should_continue_after_moderation,
        {
            "rag_agent": "intent_router",  # название ключа не меняем, чтобы не трогать логику
            "blocked": "blocked",
        },
    )

    # Intent → Query Agent
    graph.add_edge("intent_router", "query_agent")

    # Новые graph, для паралельной работы агентов
    # parallel execution
    graph.add_edge("intent_router", "rag_agent")
    graph.add_edge("intent_router", "sql_agent")
    
    # aggregation
    graph.add_edge("rag_agent", "aggregator")
    graph.add_edge("sql_agent", "aggregator")

    # Reranker над aggregated retrieved_documents
    graph.add_edge("aggregator", "reranker")
    graph.add_edge("reranker", "writer")

    graph.add_edge("blocked", END)
    graph.add_edge("writer", END)

    return graph.compile()

chat_graph = build_chat_graph()