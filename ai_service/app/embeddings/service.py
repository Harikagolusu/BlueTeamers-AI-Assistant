import time
import logging
from typing import List

from app.core.logging import request_id_var
from app.embeddings.base import BaseEmbeddingProvider
from app.embeddings.schemas import (
    EmbeddingRequest, BatchEmbeddingRequest, 
    EmbeddingResponse, BatchEmbeddingResponse
)
from app.embeddings.exceptions import InvalidInputException

logger = logging.getLogger("app.embeddings.service")

class EmbeddingService:
    """
    Business logic layer for text embedding generation.
    Handles validation, metrics, logging, and typed responses.
    Delegates ML computation to the provided BaseEmbeddingProvider.
    """
    def __init__(self, provider: BaseEmbeddingProvider):
        self.provider = provider
        
    def _get_model_info(self):
        model_name = getattr(self.provider, "model_name", "unknown")
        dimension = getattr(self.provider, "dimension", 0)
        return model_name, dimension

    def generate_embedding(self, request: EmbeddingRequest) -> EmbeddingResponse:
        start_time = time.time()
        # Fallback if contextvar isn't set (e.g. in tests)
        req_id = request_id_var.get() if request_id_var.get() != "-" else "sys"
        
        if not request.text or not request.text.strip():
            raise InvalidInputException("Text input cannot be empty.")
            
        logger.info(f"Embedding Start - ReqID: {req_id}")
        
        vector = self.provider.embed(request.text)
        model_name, dimension = self._get_model_info()
        
        process_time_ms = (time.time() - start_time) * 1000
        logger.info(f"Embedding Complete - Model: {model_name} - Dim: {dimension} - Time: {process_time_ms:.2f} ms - ReqID: {req_id}")
        
        return EmbeddingResponse(
            embedding=vector,
            dimension=dimension,
            model=model_name,
            processing_time_ms=process_time_ms
        )

    def generate_batch_embeddings(self, request: BatchEmbeddingRequest) -> BatchEmbeddingResponse:
        start_time = time.time()
        req_id = request_id_var.get() if request_id_var.get() != "-" else "sys"
        
        if not request.texts:
            raise InvalidInputException("Batch texts list cannot be empty.")
            
        for text in request.texts:
            if not text or not text.strip():
                raise InvalidInputException("Batch contains empty text strings.")
                
        batch_size = len(request.texts)
        logger.info(f"Batch Embedding Start - Size: {batch_size} - ReqID: {req_id}")
        
        vectors = self.provider.embed_batch(request.texts)
        model_name, dimension = self._get_model_info()
        
        process_time_ms = (time.time() - start_time) * 1000
        logger.info(f"Batch Embedding Complete - Model: {model_name} - Size: {batch_size} - Dim: {dimension} - Time: {process_time_ms:.2f} ms - ReqID: {req_id}")
        
        return BatchEmbeddingResponse(
            embeddings=vectors,
            dimension=dimension,
            model=model_name,
            batch_size=batch_size,
            processing_time_ms=process_time_ms
        )
