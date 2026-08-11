from fastapi import Depends
from app.embeddings.base import BaseEmbeddingProvider
from app.embeddings.provider import SentenceTransformerEmbeddingProvider
from app.embeddings.service import EmbeddingService

def get_embedding_provider() -> BaseEmbeddingProvider:
    """
    Dependency injection for the underlying embedding provider.
    Currently hard-bound to SentenceTransformer, but return type is the Base interface.
    """
    return SentenceTransformerEmbeddingProvider()

def get_embedding_service(provider: BaseEmbeddingProvider = Depends(get_embedding_provider)) -> EmbeddingService:
    """
    Dependency injection for the EmbeddingService used by routes/agents.
    """
    return EmbeddingService(provider=provider)
