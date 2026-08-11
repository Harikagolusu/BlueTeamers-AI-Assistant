from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class IndexDocumentRequest(BaseModel):
    lesson_id: str
    course_slug: str
    lesson_title: str
    content: str
    source: Optional[str] = "lesson_content"

class BatchIndexRequest(BaseModel):
    documents: List[IndexDocumentRequest]

class IndexingResult(BaseModel):
    lesson_id: str
    status: str
    chunks_generated: int
    embeddings_generated: int
    vectors_stored: int
    processing_time_ms: float
    error: Optional[str] = None

class BatchIndexResult(BaseModel):
    total_documents: int
    successful: int
    failed: int
    results: List[IndexingResult]
    total_processing_time_ms: float

class DeleteIndexRequest(BaseModel):
    lesson_id: str

class HealthResponse(BaseModel):
    status: str
    chunking_service: str
    embedding_service: str
    vector_store: str
    overall_health: bool
