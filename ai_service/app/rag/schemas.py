from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid

# Re-using context models for internal context tracking
from app.retrieval.schemas import RetrievedChunk, RetrievalRequest, RetrievalResponse
from app.context.schemas import ContextDocument, ContextResponse
from app.prompt_builder.schemas import PromptPayload, PromptResponse
from app.llm.schemas import LLMResponse

class RAGRequest(BaseModel):
    query: str
    template_name: str = "default_rag"
    metadata_filters: Optional[Dict[str, Any]] = None
    top_k: Optional[int] = None
    request_id: Optional[uuid.UUID] = Field(
        default=None, 
        description="Used exclusively for tracing, logging, and correlation across services"
    )

class SourceCitation(BaseModel):
    course: str
    lesson: str
    chunk_id: str
    similarity_score: float
    source_title: str
    source_reference: Optional[str] = None

class PipelineMetrics(BaseModel):
    retrieval_latency_ms: float = 0.0
    context_latency_ms: float = 0.0
    prompt_latency_ms: float = 0.0
    generation_latency_ms: float = 0.0
    validation_latency_ms: float = 0.0
    total_latency_ms: float = 0.0

class RAGResponse(BaseModel):
    query: str
    answer: str
    citations: List[SourceCitation]
    metrics: PipelineMetrics

class RAGContext(BaseModel):
    """
    INTERNAL USE ONLY.
    Carries the pipeline state sequentially through stages.
    """
    request_id: str
    original_request: RAGRequest
    
    # State tracking
    retrieval_response: Optional[RetrievalResponse] = None
    context_document: Optional[ContextDocument] = None
    prompt_payload: Optional[PromptPayload] = None
    llm_response: Optional[LLMResponse] = None
    
    citations: List[SourceCitation] = []
    metrics: PipelineMetrics = Field(default_factory=PipelineMetrics)
