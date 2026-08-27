from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, ClassVar
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

    # Attachment payload caps: bound worst-case vision/prompt token cost per
    # turn without affecting normal text-only conversations.
    MAX_IMAGES: ClassVar[int] = 5
    MAX_FILES: ClassVar[int] = 5
    _MAX_IMAGE_B64_CHARS: ClassVar[int] = 1_600_000   # ~1.2 MB binary per image
    _MAX_FILE_CONTENT_CHARS: ClassVar[int] = 200_000  # ~200 KB of text per file

    @field_validator('images')
    def validate_images(cls, v):
        if v and len(v) > cls.MAX_IMAGES:
            raise ValueError(f'A maximum of {cls.MAX_IMAGES} images are allowed.')
        for i, img in enumerate(v or [], start=1):
            if not isinstance(img, str) or len(img) > cls._MAX_IMAGE_B64_CHARS:
                raise ValueError(f'Image {i} exceeds the maximum allowed size.')
        return v

    @field_validator('files')
    def validate_files(cls, v):
        if v and len(v) > cls.MAX_FILES:
            raise ValueError(f'A maximum of {cls.MAX_FILES} files are allowed.')
        for i, file in enumerate(v or [], start=1):
            content = (file or {}).get('content') or ''
            if len(content) > cls._MAX_FILE_CONTENT_CHARS:
                raise ValueError(f'File {i} exceeds the maximum allowed size.')
        return v

class ChatResponse(BaseModel):
    answer: str
    citations: List[SourceCitation]
    request_id: uuid.UUID
    metrics: PipelineMetrics
