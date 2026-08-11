from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from app.retrieval.schemas import RetrievedChunk

class ContextRequest(BaseModel):
    chunks: List[RetrievedChunk]
    max_tokens: Optional[int] = None

class ContextChunk(BaseModel):
    """Represents a chunk after processing (e.g. merging, deduplication)."""
    id: str
    text: str
    score: float
    metadata: Dict[str, Any]

class ContextDocument(BaseModel):
    """The finalized context object ready to be passed to an LLM Prompt Builder."""
    chunks: List[ContextChunk]
    estimated_tokens: int
    formatted_text: str

class ContextResponse(BaseModel):
    document: ContextDocument
    original_chunk_count: int
    merged_chunk_count: int
    trimmed_chunk_count: int
    processing_time_ms: float
