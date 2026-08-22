from fastapi import Depends
from app.vector_store.base import BaseVectorStore
from app.vector_store.provider import FaissVectorStore
from app.vector_store.metadata_store import MetadataStore
from app.vector_store.service import VectorStoreService
from app.embeddings.dependencies import get_embedding_provider
from app.embeddings.base import BaseEmbeddingProvider

# Singletons for the stores
_faiss_store = FaissVectorStore()
_metadata_store = MetadataStore()

def get_vector_store() -> BaseVectorStore:
    return _faiss_store

def get_metadata_store() -> MetadataStore:
    return _metadata_store

def get_vector_store_service(
    provider: BaseVectorStore = Depends(get_vector_store),
    metadata_store: MetadataStore = Depends(get_metadata_store),
    embedding_provider: BaseEmbeddingProvider = Depends(get_embedding_provider)
) -> VectorStoreService:
    """
    Dependency injection for the VectorStoreService.
    Wires up the FAISS provider, the Metadata provider, and the ML embedding provider.
    """
    return VectorStoreService(provider, metadata_store, embedding_provider)
