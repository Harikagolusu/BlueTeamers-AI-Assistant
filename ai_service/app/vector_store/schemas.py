from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class VectorDocument(BaseModel):
    """Represents a single vector and its associated metadata to be stored."""
    id: str
    vector: List[float]
    metadata: Dict[str, Any]

class SearchRequest(BaseModel):
    """Request schema for searching the vector store."""
    query_vector: List[float]
    top_k: Optional[int] = None

class SearchResult(BaseModel):
    """Represents a single match from the vector store."""
    id: str
    score: float
    metadata: Dict[str, Any]

class SearchResponse(BaseModel):
    """Contains the array of search results and metrics."""
    results: List[SearchResult]
    processing_time_ms: float
