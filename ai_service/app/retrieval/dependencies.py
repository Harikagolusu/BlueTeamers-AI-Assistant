from fastapi import Depends

from app.embeddings.service import EmbeddingService
from app.embeddings.dependencies import get_embedding_service
from app.vector_store.service import VectorStoreService
from app.vector_store.dependencies import get_vector_store_service

from app.retrieval.reranker import BaseReranker, IdentityReranker
from app.retrieval.service import RetrievalService
from app.retrieval.base import BaseRetriever

_identity_reranker = IdentityReranker()

def get_reranker() -> BaseReranker:
    """Inject the active reranker."""
    return _identity_reranker

def get_retrieval_service(
    embedding_service: EmbeddingService = Depends(get_embedding_service),
    vector_store: VectorStoreService = Depends(get_vector_store_service),
    reranker: BaseReranker = Depends(get_reranker)
) -> BaseRetriever:
    """Wires up the retrieval dependency tree."""
    return RetrievalService(embedding_service, vector_store, reranker)
