# src/application/agents/aggregator_agent.py
from src.application.workflows.state import ChatState

def aggregator_node(state: ChatState) -> dict:
    rag_docs = state.get("rag_documents", [])
    sql_docs = state.get("sql_documents", [])

    return {
        "retrieved_documents": rag_docs + sql_docs
    }