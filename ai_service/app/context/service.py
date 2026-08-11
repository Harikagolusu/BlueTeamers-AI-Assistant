import time
import logging
from typing import List

from app.core.config import settings
from app.core.logging import request_id_var

from app.context.base import BaseContextBuilder
from app.context.builder import ContextProcessingLogic
from app.context.schemas import (
    ContextRequest, ContextChunk, ContextDocument, ContextResponse
)

logger = logging.getLogger("app.context.service")

class ContextBuilderService(BaseContextBuilder):
    """
    Orchestrates the context preparation pipeline.
    Does not call LLMs or build prompts.
    """
    def __init__(self):
        self.max_context_tokens = getattr(settings, "MAX_CONTEXT_TOKENS", 4000)

    def build_context(self, request: ContextRequest) -> ContextResponse:
        start_time = time.time()
        req_id = request_id_var.get() if request_id_var.get() != "-" else "sys"
        
        orig_count = len(request.chunks)
        max_tokens = request.max_tokens or self.max_context_tokens

        logger.info(f"Context Builder Start - Incoming Chunks: {orig_count} - ReqID: {req_id}")

        # 1. Deduplicate
        unique_chunks = ContextProcessingLogic.deduplicate(request.chunks)
        
        # 2. Merge Adjacent
        merged_chunks = ContextProcessingLogic.merge_adjacent(unique_chunks)
        merged_count = len(merged_chunks)

        # 3. Trim to Token Budget (includes sorting by score internally)
        final_chunks, total_tokens, trimmed_count = ContextProcessingLogic.trim_to_budget(
            merged_chunks, max_tokens
        )
        
        # 4. Build Structured Text
        formatted_text = ContextProcessingLogic.build_structured_context(final_chunks)

        process_ms = (time.time() - start_time) * 1000
        
        logger.info(
            f"Context Builder Complete - Tokens: {total_tokens}/{max_tokens} - "
            f"Merged: {orig_count} -> {merged_count} - Trimmed: {trimmed_count} - "
            f"Latency: {process_ms:.2f}ms - ReqID: {req_id}"
        )

        doc = ContextDocument(
            chunks=final_chunks,
            estimated_tokens=total_tokens,
            formatted_text=formatted_text
        )

        return ContextResponse(
            document=doc,
            original_chunk_count=orig_count,
            merged_chunk_count=merged_count,
            trimmed_chunk_count=trimmed_count,
            processing_time_ms=process_ms
        )

    def health_check(self) -> dict:
        return {
            "builder_status": "healthy",
            "tokenizer_status": "heuristic_estimator",
            "configuration_status": "healthy",
            "max_context_tokens": self.max_context_tokens
        }
