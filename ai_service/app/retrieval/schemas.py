from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RetrievalRequest(BaseModel):
    query: str
    top_k: Optional[int] = None
    min_score: Optional[float] = None
    metadata_filters: Optional[Dict[str, Any]] = None

class BatchRetrievalRequest(BaseModel):
    queries: List[str]
    top_k: Optional[int] = None
    min_score: Optional[float] = None
    metadata_filters: Optional[Dict[str, Any]] = None

class RetrievedChunk(BaseModel):
    chunk_id: str
    score: float
    text: str
    metadata: Dict[str, Any]

class RetrievalResponse(BaseModel):
    query_length: int
    results: List[RetrievedChunk]
    processing_time_ms: float

class HealthResponse(BaseModel):
    status: str
    embedding_service: str
    vector_store: str
    metadata_store: str
    overall_health: bool
