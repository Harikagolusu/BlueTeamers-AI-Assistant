from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional
import uuid

from app.rag.schemas import SourceCitation, PipelineMetrics

class ChatRequest(BaseModel):
    query: str = Field(..., description="The natural language query from the user")
    conversation_id: Optional[str] = Field(None, description="Optional ID for tracking conversation history")
    request_id: Optional[uuid.UUID] = Field(None, description="Optional ID for distributed tracing")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata filters for retrieval")
    images: Optional[List[str]] = Field(None, description="Optional base64 images")
    files: Optional[List[Dict[str, Any]]] = Field(None, description="Optional attached files")
    client_id: Optional[str] = Field(None, description="Persistent browser guest id for anonymous callers")
    user_id: Optional[str] = Field(None, description="Legacy client-supplied user id (ignored; identity comes from the JWT)")

    @field_validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        if len(v) > 2000:
            raise ValueError("Query length exceeds maximum limit of 2000 characters")
        return v.strip()

class ChatResponse(BaseModel):
    answer: str
    citations: List[SourceCitation]
    request_id: uuid.UUID
    metrics: PipelineMetrics
