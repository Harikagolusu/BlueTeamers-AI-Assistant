import time
import logging
from typing import List

from app.core.config import settings
from app.core.logging import request_id_var

from app.indexing.base import BaseIndexingPipeline
from app.indexing.schemas import (
    IndexDocumentRequest, BatchIndexRequest, IndexingResult, 
    BatchIndexResult, DeleteIndexRequest, HealthResponse
)
from app.indexing.exceptions import (
    ChunkingFailure, EmbeddingFailure, VectorStoreFailure, PipelineFailure
)

from app.chunking.base import BaseChunker
from app.chunking.schemas import ChunkRequest
from app.embeddings.service import EmbeddingService
from app.embeddings.schemas import BatchEmbeddingRequest
from app.vector_store.service import VectorStoreService
from app.vector_store.schemas import VectorDocument

logger = logging.getLogger("app.indexing.service")

class IndexingService(BaseIndexingPipeline):
    """
    Orchestrates Chunking -> Embedding -> Vector Store.
    Business logic and error handling boundaries exist here.
    """
    def __init__(
        self, 
        chunker: BaseChunker, 
        embedding_service: EmbeddingService, 
        vector_store: VectorStoreService
    ):
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        
        self.batch_size = getattr(settings, "INDEX_BATCH_SIZE", 10)
        self.max_concurrent = getattr(settings, "MAX_CONCURRENT_DOCUMENTS", 5)
        self.retry_count = getattr(settings, "RETRY_COUNT", 3)

    def _delete_lesson_chunks(self, lesson_id: str) -> None:
        """
        Helper to find and delete all chunks belonging to a specific lesson.
        Scans metadata store since FAISS doesn't natively support querying by payload.
        """
        meta_store = self.vector_store.metadata_store
        # We need to lock while reading to safely iterate if concurrency is high
        # To avoid deadlocks, we fetch all items, then issue deletes.
        with meta_store._lock:
            all_items = list(meta_store.metadata.items())
            
        chunks_to_delete = [
            chunk_id for chunk_id, meta in all_items 
            if meta.get("lesson_id") == lesson_id
        ]
        
        for cid in chunks_to_delete:
            self.vector_store.delete(cid)
            
        logger.info(f"Deleted {len(chunks_to_delete)} existing chunks for lesson {lesson_id}.")

    def index_document(self, request: IndexDocumentRequest) -> IndexingResult:
        start_time = time.time()
        req_id = request_id_var.get() if request_id_var.get() != "-" else "sys"
        
        logger.info(f"Indexing Pipeline Start - Lesson: {request.lesson_id} - ReqID: {req_id}")
        
        try:
            # 1. Chunking
            try:
                chunk_req = ChunkRequest(
                    content=request.content,
                    course_slug=request.course_slug,
                    lesson_id=request.lesson_id,
                    lesson_title=request.lesson_title,
                    source=request.source
                )
                chunk_res = self.chunker.chunk(chunk_req)
            except Exception as e:
                raise ChunkingFailure(f"Failed to chunk document: {str(e)}")

            if chunk_res.total_chunks == 0:
                logger.warning(f"No chunks generated for {request.lesson_id}.")
                return IndexingResult(
                    lesson_id=request.lesson_id, status="success",
                    chunks_generated=0, embeddings_generated=0, vectors_stored=0,
                    processing_time_ms=(time.time()-start_time)*1000
                )

            # 2. Embedding
            try:
                texts = [c.text for c in chunk_res.chunks]
                embed_req = BatchEmbeddingRequest(texts=texts)
                embed_res = self.embedding_service.generate_batch_embeddings(embed_req)
            except Exception as e:
                raise EmbeddingFailure(f"Failed to generate embeddings: {str(e)}")

            # 3. Vector Storage
            try:
                docs = []
                for chunk, vector in zip(chunk_res.chunks, embed_res.embeddings):
                    docs.append(VectorDocument(
                        id=chunk.metadata.chunk_id,
                        vector=vector,
                        # Metadata is highly typed but VectorStore expects Dict
                        metadata=chunk.metadata.model_dump()
                    ))
                self.vector_store.add_documents(docs)
                # Ensure it flushes to disk immediately for persistence
                self.vector_store.save()
            except Exception as e:
                raise VectorStoreFailure(f"Failed to store vectors: {str(e)}")

            process_time = (time.time() - start_time) * 1000
            
            logger.info(f"Indexing Pipeline Complete - Lesson: {request.lesson_id} "
                        f"Chunks: {chunk_res.total_chunks} Vectors: {len(docs)} "
                        f"Time: {process_time:.2f}ms ReqID: {req_id}")

            return IndexingResult(
                lesson_id=request.lesson_id,
                status="success",
                chunks_generated=chunk_res.total_chunks,
                embeddings_generated=len(embed_res.embeddings),
                vectors_stored=len(docs),
                processing_time_ms=process_time
            )
            
        except Exception as e:
            logger.error(f"Indexing Pipeline Failed - Lesson: {request.lesson_id} Error: {str(e)}")
            return IndexingResult(
                lesson_id=request.lesson_id,
                status="failed",
                chunks_generated=0, embeddings_generated=0, vectors_stored=0,
                processing_time_ms=(time.time() - start_time) * 1000,
                error=str(e)
            )

    def index_documents(self, request: BatchIndexRequest) -> BatchIndexResult:
        start_time = time.time()
        results = []
        success = 0
        failed = 0
        
        # Process incrementally to avoid massive memory spikes
        for doc in request.documents:
            res = self.index_document(doc)
            results.append(res)
            if res.status == "success":
                success += 1
            else:
                failed += 1
                
        # Optional: could use max_concurrent to ThreadPoolExecutor this, 
        # but standard incremental for loop satisfies core requirement.
        
        return BatchIndexResult(
            total_documents=len(request.documents),
            successful=success,
            failed=failed,
            results=results,
            total_processing_time_ms=(time.time() - start_time) * 1000
        )

    def update_document(self, request: IndexDocumentRequest) -> IndexingResult:
        """Updates by explicitly deleting old chunks then reindexing."""
        try:
            self._delete_lesson_chunks(request.lesson_id)
            return self.index_document(request)
        except Exception as e:
            logger.error(f"Failed to update document {request.lesson_id}: {str(e)}")
            return IndexingResult(
                lesson_id=request.lesson_id, status="failed",
                chunks_generated=0, embeddings_generated=0, vectors_stored=0,
                processing_time_ms=0.0, error=str(e)
            )

    def delete_document(self, request: DeleteIndexRequest) -> bool:
        try:
            self._delete_lesson_chunks(request.lesson_id)
            self.vector_store.save()
            return True
        except Exception as e:
            logger.error(f"Failed to delete document {request.lesson_id}: {str(e)}")
            return False

    def reindex(self, request: BatchIndexRequest) -> BatchIndexResult:
        # Reindexing essentially drops everything (or targeted) and adds them.
        # For targeted reindex, we can just call update_document in a loop.
        start_time = time.time()
        results = []
        success = 0
        failed = 0
        
        for doc in request.documents:
            res = self.update_document(doc)
            results.append(res)
            if res.status == "success":
                success += 1
            else:
                failed += 1
                
        return BatchIndexResult(
            total_documents=len(request.documents),
            successful=success,
            failed=failed,
            results=results,
            total_processing_time_ms=(time.time() - start_time) * 1000
        )

    def health_check(self) -> HealthResponse:
        # Mock simple checks for external components
        try:
            ch_status = "healthy" if self.chunker else "unhealthy"
            
            # Embeddings health
            emb_h = self.embedding_service.provider.health_check()
            emb_status = emb_h.get("status", "unknown")
            
            # Vector Store health
            vs_h = self.vector_store.get_health()
            vs_status = "healthy" if vs_h.get("loaded") else "unhealthy"
            
            overall = ch_status == "healthy" and emb_status == "healthy" and vs_status == "healthy"
            
            return HealthResponse(
                status="healthy" if overall else "degraded",
                chunking_service=ch_status,
                embedding_service=emb_status,
                vector_store=vs_status,
                overall_health=overall
            )
        except Exception as e:
            return HealthResponse(
                status="unhealthy",
                chunking_service="error",
                embedding_service="error",
                vector_store="error",
                overall_health=False
            )
