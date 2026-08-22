import time
import logging
from typing import List

from app.core.config import settings
from app.core.logging import request_id_var
from app.vector_store.base import BaseVectorStore
from app.vector_store.metadata_store import MetadataStore
from app.vector_store.schemas import (
    VectorDocument, SearchRequest, SearchResult, SearchResponse
)
from app.embeddings.base import BaseEmbeddingProvider

logger = logging.getLogger("app.vector_store.service")

class VectorStoreService:
    """
    Business logic orchestrator joining the pure FAISS vector operations 
    with the JSON Metadata Store, providing a seamless abstraction.
    """
    def __init__(
        self, 
        provider: BaseVectorStore, 
        metadata_store: MetadataStore,
        embedding_provider: BaseEmbeddingProvider
    ):
        self.provider = provider
        self.metadata_store = metadata_store
        self.embedding_provider = embedding_provider
        self.top_k_default = getattr(settings, "TOP_K_DEFAULT", 5)
        
        self._initialize_store()
        
    def _initialize_store(self):
        """Attempts to load the store. If empty, creates a new one dynamically detecting dimensions."""
        start = time.time()
        self.provider.load()
        self.metadata_store.load()
        
        # If not loaded, we generate the index dynamically from the active embedding model
        if not self.provider.health_check()["loaded"]:
            self.embedding_provider.load_model()
            dim = self.embedding_provider.health_check().get("embedding_dimension")
            if dim:
                self.provider.initialize(dimension=dim)
            else:
                logger.warning("VectorStoreService could not auto-detect embedding dimensions.")
                
        logger.info(f"Vector Store Initialization Latency: {(time.time() - start) * 1000:.2f} ms")

    def add_document(self, doc: VectorDocument) -> None:
        self.provider.add(doc.id, doc.vector)
        self.metadata_store.update(doc.id, doc.metadata)
        logger.info(f"Vector Store: Added 1 vector. ReqID: {request_id_var.get()}")

    def add_documents(self, docs: List[VectorDocument]) -> None:
        if not docs:
            return
        
        ids = [doc.id for doc in docs]
        vectors = [doc.vector for doc in docs]
        
        self.provider.add_batch(ids, vectors)
        for doc in docs:
            self.metadata_store.update(doc.id, doc.metadata)
            
        logger.info(f"Vector Store: Added {len(docs)} vectors. ReqID: {request_id_var.get()}")

    def search(self, request: SearchRequest) -> SearchResponse:
        start_time = time.time()
        top_k = request.top_k or self.top_k_default
        
        ids, scores = self.provider.search(request.query_vector, top_k)
        
        results = []
        for vid, score in zip(ids, scores):
            meta = self.metadata_store.get(vid) or {}
            results.append(SearchResult(id=vid, score=score, metadata=meta))
            
        process_ms = (time.time() - start_time) * 1000
        logger.info(f"Vector Store: Search Latency {process_ms:.2f} ms, Top K: {top_k}. ReqID: {request_id_var.get()}")
        
        return SearchResponse(
            results=results,
            processing_time_ms=process_ms
        )

    def delete(self, id: str) -> None:
        self.provider.delete(id)
        self.metadata_store.delete(id)

    def save(self) -> None:
        start = time.time()
        self.provider.save()
        self.metadata_store.save()
        logger.info(f"Vector Store: Save Latency {(time.time() - start) * 1000:.2f} ms")
        
    def get_health(self) -> dict:
        health = self.provider.health_check()
        health["metadata_count"] = self.metadata_store.count()
        return health
