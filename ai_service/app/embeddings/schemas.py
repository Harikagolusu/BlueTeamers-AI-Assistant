from pydantic import BaseModel
from typing import List, Optional

class EmbeddingRequest(BaseModel):
    """Request schema for a single text embedding."""
    text: str
    
class BatchEmbeddingRequest(BaseModel):
    """Request schema for batch text embeddings."""
    texts: List[str]

class EmbeddingResponse(BaseModel):
    """Response schema containing the vector representation."""
    embedding: List[float]
    dimension: int
    model: str
    processing_time_ms: float

class BatchEmbeddingResponse(BaseModel):
    """Response schema containing multiple vector representations."""
    embeddings: List[List[float]]
    dimension: int
    model: str
    batch_size: int
    processing_time_ms: float
