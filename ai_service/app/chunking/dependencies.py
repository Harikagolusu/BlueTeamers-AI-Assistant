from fastapi import Depends
from app.core.config import settings
from app.chunking.base import BaseChunker
from app.chunking.schemas import ChunkingConfig
from app.chunking.chunker import MarkdownRecursiveChunker

def get_chunking_config() -> ChunkingConfig:
    """
    Provides the ChunkingConfig object hydrated from the environment settings.
    """
    return ChunkingConfig(
        chunk_size=getattr(settings, "CHUNK_SIZE", 600),
        chunk_overlap=getattr(settings, "CHUNK_OVERLAP", 120),
        max_document_size_mb=getattr(settings, "MAX_DOCUMENT_SIZE_MB", 5)
    )

def get_chunker(config: ChunkingConfig = Depends(get_chunking_config)) -> BaseChunker:
    """
    Dependency injection for the Chunking Service.
    Returns the BaseChunker interface, decoupling the actual implementation.
    """
    return MarkdownRecursiveChunker(config=config)
