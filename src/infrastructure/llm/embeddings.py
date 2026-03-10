# from langchain_openai import OpenAIEmbeddings
# from src.config.settings import settings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_google_genai import GoogleGenerativeAIEmbeddings


# def get_embeddings():
#     kwargs = {
#         "model": settings.embedding_model,
#         "dimensions": settings.embedding_dimensions,
#         "api_key": settings.openai_api_key,
#     }
#     if settings.embedding_base_url:
#         kwargs["base_url"] = settings.embedding_base_url
#     return OpenAIEmbeddings(**kwargs)


# def get_embeddings():
#     if settings.embedding_provider == "google":
#         return GoogleGenerativeAIEmbeddings(
#             model=settings.embedding_model,
#             google_api_key=settings.google_api_key,
#             task_type="retrieval_document",
#         )

    # from langchain_openai import OpenAIEmbeddings
    # return OpenAIEmbeddings(
    #     model=settings.embedding_model,
    #     dimensions=settings.embedding_dimensions,
    #     api_key=settings.openai_api_key,
    # )

from src.config.settings import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings

def get_embeddings(task_type: str = "retrieval_document"):
    """
    task_type="retrieval_document" — при ingestion (записываем документы)
    task_type="retrieval_query"    — при поиске (запрос пользователя)
    """
    # if settings.embedding_provider == "google":
    if settings.embedding_provider in ("google", "google_genai"):
        
        return GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
            task_type=task_type,
        )

    return OpenAIEmbeddings(
        model=settings.embedding_model,
        dimensions=settings.embedding_dimensions,
        api_key=settings.openai_api_key,
    )