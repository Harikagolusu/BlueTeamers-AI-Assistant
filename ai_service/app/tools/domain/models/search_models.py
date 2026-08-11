from pydantic import BaseModel, Field
from typing import Dict, Any

class SearchDocument(BaseModel):
    id: str = Field(..., description="Unique document ID")
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content snippet")
    score: float = Field(..., description="Relevance score (e.g. 0.0 - 1.0)")
    source: str = Field(..., description="Origin of the document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
