import logging
import time
import re
from typing import List

from app.core.logging import request_id_var
from app.chunking.base import BaseChunker
from app.chunking.schemas import Chunk, ChunkRequest, ChunkResponse, ChunkingConfig
from app.chunking.exceptions import EmptyContentException, OversizedContentException
from app.chunking.metadata import MetadataGenerator

logger = logging.getLogger("app.chunking.chunker")

class MarkdownRecursiveChunker(BaseChunker):
    """
    Enterprise chunker that processes Markdown documents while preserving structural
    integrity (e.g., keeping code blocks, tables, and lists intact).
    """
    
    def __init__(self, config: ChunkingConfig):
        """
        Initializes the chunker with the provided configuration object.
        LangChain dependencies are isolated to this class.
        """
        self.config = config
        
        # Encapsulate LangChain strictly inside this provider logic
        try:
            from langchain_text_splitters import MarkdownTextSplitter
        except ImportError:
            from langchain.text_splitter import MarkdownTextSplitter
            
        self.splitter = MarkdownTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap
        )

    def clean_text(self, text: str) -> str:
        """
        Removes unnecessary excessive whitespace while preserving the semantic 
        structure of the Markdown.
        """
        if not text:
            return ""
            
        # Replace 3 or more consecutive newlines with exactly 2
        cleaned = re.sub(r'\n{3,}', '\n\n', text)
        return cleaned.strip()

    def validate(self, text: str) -> bool:
        """
        Validates the text size and content against the configured constraints.
        """
        if not text or len(text.strip()) == 0:
            raise EmptyContentException("Lesson content is empty.")
            
        max_size_bytes = self.config.max_document_size_mb * 1024 * 1024
        if len(text) > max_size_bytes:
            raise OversizedContentException(f"Content exceeds maximum allowed size ({self.config.max_document_size_mb}MB).")
            
        return True

    def chunk(self, request: ChunkRequest) -> ChunkResponse:
        """
        Orchestrates the validation, cleaning, and text splitting.
        Returns a strongly-typed ChunkResponse.
        """
        start_time = time.time()
        # request_id_var might not be set in tests, provide fallback
        req_id = request_id_var.get() if request_id_var.get() != "-" else "test-env"
        
        logger.info(f"Chunking Started - Lesson: {request.lesson_id} - ReqID: {req_id}")
        
        try:
            self.validate(request.content)
            
            cleaned_text = self.clean_text(request.content)
            text_chunks = self.splitter.split_text(cleaned_text)
            
            chunks: List[Chunk] = []
            for i, chunk_text in enumerate(text_chunks):
                metadata = MetadataGenerator.generate(request, chunk_index=i)
                chunks.append(Chunk(text=chunk_text, metadata=metadata))
                
            total_chunks = len(chunks)
            process_time_ms = (time.time() - start_time) * 1000
            
            logger.info(
                f"Chunking Completed - Lesson: {request.lesson_id} - "
                f"Chunks: {total_chunks} - Time: {process_time_ms:.2f} ms - ReqID: {req_id}"
            )
            
            return ChunkResponse(
                lesson_id=request.lesson_id,
                total_chunks=total_chunks,
                chunks=chunks
            )
            
        except Exception as e:
            logger.error(f"Chunking Failed - Lesson: {request.lesson_id} - Error: {str(e)} - ReqID: {req_id}")
            raise
