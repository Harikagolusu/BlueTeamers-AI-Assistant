"""
Dependency wiring for the knowledge ingestion pipeline.

Reuses the same FAISS + metadata + embedding singletons used by the chat
bootstrap so the runtime query path and the ingestion path share one store.
"""

from fastapi import Depends

from app.embeddings.base import BaseEmbeddingProvider
from app.embeddings.dependencies import get_embedding_provider
from app.vector_store.base import BaseVectorStore
from app.vector_store.dependencies import get_vector_store, get_metadata_store
from app.vector_store.metadata_store import MetadataStore
from app.vector_store.service import VectorStoreService
from app.knowledge.pipeline import KnowledgeIngestionPipeline


def get_vector_store_service_for_knowledge(
    provider: BaseVectorStore = Depends(get_vector_store),
    metadata_store: MetadataStore = Depends(get_metadata_store),
    embedding_provider: BaseEmbeddingProvider = Depends(get_embedding_provider),
) -> VectorStoreService:
    return VectorStoreService(provider, metadata_store, embedding_provider)


# Module-level singleton so ingest/status share state and only load the model once.
_pipeline: "KnowledgeIngestionPipeline" = None


def get_knowledge_pipeline(
    vector_store: VectorStoreService = Depends(get_vector_store_service_for_knowledge),
    embedding_provider: BaseEmbeddingProvider = Depends(get_embedding_provider),
) -> KnowledgeIngestionPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = KnowledgeIngestionPipeline(vector_store, embedding_provider)
    return _pipeline
