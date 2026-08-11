from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Optional, List
from app.rag.schemas import SourceCitation, PipelineMetrics

class StreamEventType(str, Enum):
    TOKEN = "token"
    COMPLETION = "completion"
    ERROR = "error"

class TokenEvent(BaseModel):
    content: str

class CompletionEvent(BaseModel):
    citations: List[SourceCitation]
    metrics: PipelineMetrics

class ErrorEvent(BaseModel):
    detail: str

class StreamEvent(BaseModel):
    event: StreamEventType
    data: Any
