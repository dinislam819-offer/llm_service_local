# src/application/agents/aggregator_agent.py
from src.application.workflows.state import ChatState

def aggregator_node(state: ChatState) -> dict:
    rag_docs = state.get("rag_documents", [])
    sql_docs = state.get("sql_documents", [])

    return {
        "retrieved_documents": rag_docs + sql_docs
    }

# def aggregator_node(state: ChatState) -> dict:
#     rag_docs = state.get("rag_documents", [])
#     sql_docs = state.get("sql_documents", [])

#     combined = rag_docs + sql_docs

#     # сортировка по score
#     combined.sort(key=lambda x: x.get("score", 0), reverse=True)

#     # threshold + top-k
#     filtered = [doc for doc in combined if doc.get("score", 0) >= 0.5][:10]

#     return {
#         "retrieved_documents": filtered
#     }



# новая логика надо проверить
# import logging
# from src.application.workflows.state import ChatState

# logger = logging.getLogger(__name__)


# def aggregator_node(state: ChatState) -> dict:
#     rag_docs = state.get("rag_documents") or []
#     sql_docs = state.get("sql_documents") or []

#     logger.warning(
#         "AGGREGATOR: rag_docs=%d, sql_docs=%d",
#         len(rag_docs),
#         len(sql_docs),
#     )

#     # Помечаем источник каждого документа
#     for doc in rag_docs:
#         doc.setdefault("source", "rag")

#     for doc in sql_docs:
#         doc.setdefault("source", "sql")

#     combined = rag_docs + sql_docs

#     # Сортируем только RAG-документы по score (у SQL его нет)
#     # SQL-документы всегда проходят — они уже отфильтрованы SQL-запросом
#     combined.sort(
#         key=lambda x: x.get("score", 1.0),  # у SQL score=1.0 (максимум)
#         reverse=True
#     )

#     # Берём top-10 без threshold (SQL уже отфильтрован WHERE-условиями)
#     topk = combined[:10]

#     logger.warning(
#         "AGGREGATOR: combined=%d, after_topk=%d",
#         len(combined),
#         len(topk),
#     )

#     return {"retrieved_documents": topk}