"""
Knowledge ingestion pipeline for the Hybrid Knowledge Architecture.

    Document Loader  ->  Chunking  ->  Cleaning  ->  Embedding  ->  Vector Store
          (sources)   (markdown chunker)  (clean_text)  (bge-small-en-v1.5)   (FAISS)

Supports incremental indexing: every chunk carries a deterministic id and a
`content_hash`. On re-run, unchanged chunks are skipped (no re-embedding), and
changed chunks are re-embedded in place. Only static knowledge is ingested —
dynamic platform data is never embedded.
"""

import hashlib
import logging
from typing import Dict, Any, List, Optional

from app.core.config import settings
from app.chunking.chunker import MarkdownRecursiveChunker
from app.chunking.schemas import ChunkingConfig, ChunkRequest
from app.embeddings.base import BaseEmbeddingProvider
from app.vector_store.service import VectorStoreService
from app.vector_store.schemas import VectorDocument

from app.knowledge.sources import (
    build_all_static_documents,
    build_course_level_documents,
    build_lesson_documents,
)

logger = logging.getLogger("app.knowledge.pipeline")


class KnowledgeIngestionPipeline:
    def __init__(
        self,
        vector_store: VectorStoreService,
        embedding_provider: BaseEmbeddingProvider,
    ):
        self._vector_store = vector_store
        self._embedding_provider = embedding_provider
        self._chunker = MarkdownRecursiveChunker(ChunkingConfig(
            chunk_size=getattr(settings, "CHUNK_SIZE", 600),
            chunk_overlap=getattr(settings, "CHUNK_OVERLAP", 120),
            max_document_size_mb=getattr(settings, "MAX_DOCUMENT_SIZE_MB", 5),
        ))

    # ------------------------------------------------------------------ #
    # Chunking
    # ------------------------------------------------------------------ #
    def _chunk_lesson(self, lesson_doc: Dict[str, Any]) -> List[VectorDocument]:
        meta = lesson_doc["metadata"]
        request = ChunkRequest(
            content=lesson_doc["text"],
            course_slug=meta["course_slug"],
            lesson_id=meta["lesson_id"],
            lesson_title=meta.get("lesson_title", ""),
            source=meta.get("source", "lesson_content"),
        )
        response = self._chunker.chunk(request)
        vectors: List[VectorDocument] = []
        for chunk in response.chunks:
            text = chunk.text
            cmeta = chunk.metadata
            vectors.append(VectorDocument(
                id=cmeta.chunk_id,
                vector=[],  # filled during embedding
                metadata={
                    "kind": "lesson_chunk",
                    "text": text,
                    "course_slug": cmeta.course_slug,
                    "course_id": meta.get("course_id", ""),
                    "course_title": meta.get("course_title", ""),
                    "lesson_id": cmeta.lesson_id,
                    "lesson_title": cmeta.lesson_title,
                    "source": cmeta.source,
                    "chunk_index": cmeta.chunk_index,
                    "content_hash": hashlib.sha1(text.encode("utf-8")).hexdigest(),
                },
            ))
        return vectors

    def _as_vector(self, doc: Dict[str, Any]) -> VectorDocument:
        meta = doc["metadata"]
        return VectorDocument(
            id=doc["doc_id"],
            vector=[],  # filled during embedding
            metadata={
                "kind": meta.get("kind", "document"),
                "text": doc["text"],
                "course_slug": meta.get("course_slug", ""),
                "course_id": meta.get("course_id", ""),
                "course_title": meta.get("course_title", ""),
                "lesson_id": meta.get("lesson_id", ""),
                "lesson_title": meta.get("lesson_title", ""),
                "source": meta.get("source", "document"),
                "content_hash": meta.get("content_hash", ""),
            },
        )

    # ------------------------------------------------------------------ #
    # Incremental diffing
    # ------------------------------------------------------------------ #
    def _needs_index(self, doc: VectorDocument) -> bool:
        """True if the chunk is new or its content changed (content_hash mismatch)."""
        existing = self._vector_store.metadata_store.get(doc.id)
        if existing is None:
            return True
        return existing.get("content_hash") != doc.metadata.get("content_hash")

    def _upsert_docs(self, docs: List[VectorDocument]) -> Dict[str, int]:
        new_docs: List[VectorDocument] = []
        reindexed = 0
        skipped = 0
        for doc in docs:
            if not self._needs_index(doc):
                skipped += 1
                continue
            # Re-embed changed chunks in place
            if self._vector_store.metadata_store.get(doc.id) is not None:
                self._vector_store.delete(doc.id)
                reindexed += 1
            new_docs.append(doc)

        if not new_docs:
            return {"added": 0, "reindexed": reindexed, "skipped": skipped}

        texts = [d.metadata["text"] for d in new_docs]
        vectors = self._embedding_provider.embed_batch(texts)
        for doc, vector in zip(new_docs, vectors):
            doc.vector = vector
        self._vector_store.add_documents(new_docs)
        return {"added": len(new_docs), "reindexed": reindexed, "skipped": skipped}

    # ------------------------------------------------------------------ #
    # Orchestration
    # ------------------------------------------------------------------ #
    def ingest(self) -> Dict[str, Any]:
        """Runs the full ingestion pipeline. Idempotent & incremental."""
        logger.info("Knowledge ingestion started.")

        course_docs = [self._as_vector(d) for d in build_course_level_documents()]
        lesson_vectors: List[VectorDocument] = []
        for lesson_doc in build_lesson_documents():
            lesson_vectors.extend(self._chunk_lesson(lesson_doc))

        logger.info(f"Prepared {len(course_docs)} course docs, {len(lesson_vectors)} lesson chunks.")

        summary = {"course_overviews": self._upsert_docs(course_docs)}
        lesson_summary = self._upsert_docs(lesson_vectors)
        summary["lesson_chunks"] = lesson_summary

        self._vector_store.save()
        total = self._vector_store.metadata_store.count()
        logger.info(f"Knowledge ingestion complete. Total vectors in store: {total} -> {summary}")
        return {**summary, "total_vectors": total}

    def status(self) -> Dict[str, Any]:
        return {
            "vector_count": self._vector_store.metadata_store.count(),
            "loaded": self._vector_store.get_health().get("loaded", False),
        }
