# src/application/agents/reranker_agent.py
import json
from langchain_core.messages import HumanMessage
from src.core.llm import get_llm
from src.application.workflows.state import ChatState

import logging

logger = logging.getLogger(__name__)

_llm = get_llm()

_RERANK_PROMPT = """Ты — агент ранжирования документов.
По запросу и списку фрагментов отсортируй их по релевантности.
Верни JSON:
[
  {"index": 0, "score": 0.95},
  ...
]

Запрос:
{query}

Фрагменты:
{docs}
"""


async def reranker_node(state: ChatState) -> ChatState:
    """Переупорядочивает объединённые документы по релевантности и обрезает хвост."""
    docs = state.get("retrieved_documents") or []
    if not docs:
        logger.debug("RERANKER: no documents to rerank")
        return state

    # Чтобы не ранжировать повторно, если узел вызовут ещё раз
    if state.get("reranked"):
        logger.debug("RERANKER: already reranked, skipping")
        return state

    query = state.get("rewritten_query") or state["messages"][-1].content
    logger.debug(
        "RERANKER: start, query=%r, docs_count=%d",
        query,
        len(docs),
    )

    # предполагаем, что у документа есть поле "text"
    docs_text = "\n\n".join(
        f"[{i}] {d['text']}" for i, d in enumerate(docs)
    )

    prompt = _RERANK_PROMPT.format(query=query, docs=docs_text)
    resp = await _llm.ainvoke([HumanMessage(content=prompt)])

    try:
        ranking = json.loads(resp.content)
        ordered = sorted(ranking, key=lambda x: x["score"], reverse=True)
        topk = ordered[:5]  # можно вынести 5 в настройку


        new_docs = [docs[item["index"]] for item in topk]
        logger.debug(
            "RERANKER: reranked, original_count=%d, new_count=%d, top_indices=%s",
            len(docs),
            len(new_docs),
            [item["index"] for item in topk],
        )

        state["retrieved_documents"] = [docs[item["index"]] for item in topk]
        state["reranked"] = True
    except Exception:
        # если JSON кривой — оставляем исходный порядок
        logger.warning(
            "RERANKER: failed to parse ranking JSON, error=%r, raw_response=%r",
            exc,
            resp.content,
        )
        return state

    return state