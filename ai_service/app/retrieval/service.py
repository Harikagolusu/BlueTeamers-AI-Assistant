import time
import logging
from typing import List

from app.core.config import settings
from app.core.logging import request_id_var

from app.retrieval.base import BaseRetriever
from app.retrieval.reranker import BaseReranker
from app.retrieval.schemas import (
    RetrievalRequest, BatchRetrievalRequest, 
    RetrievedChunk, RetrievalResponse, HealthResponse
)
from app.retrieval.exceptions import (
    EmbeddingFailure, SearchFailure, MetadataFailure, RetrievalException
)

from app.embeddings.service import EmbeddingService
from app.embeddings.schemas import EmbeddingRequest
from app.vector_store.service import VectorStoreService
from app.vector_store.schemas import SearchRequest as VSearchRequest

logger = logging.getLogger("app.retrieval.service")

class RetrievalService(BaseRetriever):
    """
    Orchestrates Query -> Embeddings -> Vector Store -> Metadata -> Reranker.
    Does not implement LLM generation.
    """
    def __init__(
        self, 
        embedding_service: EmbeddingService, 
        vector_store: VectorStoreService,
        reranker: BaseReranker
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.reranker = reranker
        
        self.default_top_k = getattr(settings, "DEFAULT_TOP_K", 5)
        self.max_top_k = getattr(settings, "MAX_TOP_K", 20)
        self.min_similarity_score = getattr(settings, "MIN_SIMILARITY_SCORE", 0.0)

    def retrieve(self, request: RetrievalRequest) -> RetrievalResponse:
        start_time = time.time()
        req_id = request_id_var.get() if request_id_var.get() != "-" else "sys"
        query_len = len(request.query)
        
        # 1. Parameter resolution
        top_k = request.top_k if request.top_k is not None else self.default_top_k
        top_k = min(top_k, self.max_top_k)
        min_score = request.min_score if request.min_score is not None else self.min_similarity_score
        
        logger.info(f"Retrieval Start - Len: {query_len}, TopK: {top_k} - ReqID: {req_id}")

        # 2. Embedding Generation
        emb_start = time.time()
        try:
            emb_req = EmbeddingRequest(text=request.query)
            emb_res = self.embedding_service.generate_embedding(emb_req)
        except Exception as e:
            raise EmbeddingFailure(f"Failed to generate query embedding: {str(e)}")
        emb_lat = (time.time() - emb_start) * 1000

        # 3. Vector Store Search
        vs_start = time.time()
        try:
            vs_req = VSearchRequest(query_vector=emb_res.embedding, top_k=top_k)
            vs_res = self.vector_store.search(vs_req)
        except Exception as e:
            raise SearchFailure(f"Failed to search vector store: {str(e)}")
        vs_lat = (time.time() - vs_start) * 1000

        # 4. Metadata Mapping & Filtering
        meta_start = time.time()
        try:
            raw_chunks = []
            for item in vs_res.results:
                # Filter by similarity threshold
                if item.score < min_score:
                    continue
                    
                # Optional metadata filtering (future-ready placeholder)
                if request.metadata_filters:
                    # Simple matching simulation: values may be scalars
                    # (strict equality) or lists/tuples (membership, e.g.
                    # filtering by a set of enrolled course slugs).
                    match = True
                    for k, v in request.metadata_filters.items():
                        if isinstance(v, (list, tuple, set)):
                            if item.metadata.get(k) not in v:
                                match = False
                                break
                        elif item.metadata.get(k) != v:
                            match = False
                            break
                    if not match:
                        continue
                
                # We assume text is either passed back directly from FAISS via VectorStoreService metadata 
                # mapping or we extract it. The Chunk metadata inherently captures it or we can fallback.
                # Since chunk text is normally part of the VectorDocument metadata stored previously.
                text_content = item.metadata.get("text", "") 
                if not text_content:
                    # Fallback check if it was placed elsewhere or just log
                    text_content = item.metadata.get("content", "")
                    
                raw_chunks.append(RetrievedChunk(
                    chunk_id=item.id,
                    score=item.score,
                    text=text_content,
                    metadata=item.metadata
                ))
        except Exception as e:
            raise MetadataFailure(f"Failed to map metadata: {str(e)}")
        
        # 5. Reranking
        ranked_chunks = self.reranker.rerank(request.query, raw_chunks)
        
        total_time = (time.time() - start_time) * 1000
        logger.info(
            f"Retrieval Complete - Latency: {total_time:.2f}ms (Emb: {emb_lat:.2f}ms, VS: {vs_lat:.2f}ms) "
            f"- Retrieved: {len(ranked_chunks)} - ReqID: {req_id}"
        )
        
        return RetrievalResponse(
            query_length=query_len,
            results=ranked_chunks,
            processing_time_ms=total_time
        )

    def retrieve_batch(self, request: BatchRetrievalRequest) -> List[RetrievalResponse]:
        # Process iteratively. Can be optimized in the future by doing a batch embedding first,
        # but iterating ensures strict boundary adherence and avoids massive memory blocks for now.
        responses = []
        for q in request.queries:
            req = RetrievalRequest(
                query=q, 
                top_k=request.top_k, 
                min_score=request.min_score, 
                metadata_filters=request.metadata_filters
            )
            # We don't swallow exceptions here normally unless we want partial failure at retrieval.
            # Usually retrieval is blocking, so we let exceptions bubble or wrap them.
            try:
                responses.append(self.retrieve(req))
            except Exception as e:
                logger.error(f"Batch Retrieval Partial Failure: {str(e)}")
                raise # Re-raise to let the caller handle it based on requirements
        return responses

    def health_check(self) -> HealthResponse:
        try:
            emb_h = self.embedding_service.provider.health_check()
            emb_status = emb_h.get("status", "unknown")
            
            vs_h = self.vector_store.get_health()
            vs_status = "healthy" if vs_h.get("loaded") else "unhealthy"
            
            # Since vector_store wraps metadata_store, we infer its health
            meta_status = "healthy" if vs_h.get("metadata_count", -1) >= 0 else "unhealthy"
            
            overall = emb_status == "healthy" and vs_status == "healthy" and meta_status == "healthy"
            
            return HealthResponse(
                status="healthy" if overall else "degraded",
                embedding_service=emb_status,
                vector_store=vs_status,
                metadata_store=meta_status,
                overall_health=overall
            )
        except Exception:
            return HealthResponse(
                status="unhealthy",
                embedding_service="error",
                vector_store="error",
                metadata_store="error",
                overall_health=False
            )
