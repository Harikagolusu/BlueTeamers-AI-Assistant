from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ExecutionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"

from pydantic import ConfigDict

class ExecutionResult(BaseModel):
    """
    Standardizes all engine outputs, vastly simplifying ResponseComposition.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status: ExecutionStatus = Field(..., description="The outcome of the execution engine")
    engine_name: str = Field(..., description="Name of the engine that produced this result")
    
    message: str = Field(default="", description="The final text response or synthesis")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Engine specific metadata")
    citations: List[Dict[str, Any]] = Field(default_factory=list, description="Citations used for the response")
    tool_outputs: List[Dict[str, Any]] = Field(default_factory=list, description="Raw outputs from Tool Calling Framework")
    documents: List[Dict[str, Any]] = Field(default_factory=list, description="Raw documents retrieved by RAG")
    
    reasoning_metadata: Dict[str, Any] = Field(default_factory=dict, description="Internal reasoning steps (e.g. CoT)")
    
    latency_ms: float = Field(default=0.0, description="Execution time in milliseconds")
    cost: float = Field(default=0.0, description="Estimated cost of execution")
    token_usage: Dict[str, int] = Field(default_factory=dict, description="Token consumption metrics")
    
    errors: List[Dict[str, Any]] = Field(default_factory=list, description="Non-fatal or fatal errors encountered")
    stream: bool = Field(default=False, description="Indicates if this result is meant to be a stream generator")
    
    @classmethod
    def success(cls, engine: str, message: str, **kwargs) -> "ExecutionResult":
        return cls(status=ExecutionStatus.SUCCESS, engine_name=engine, message=message, **kwargs)
    
    @classmethod
    def failed(cls, engine: str, errors: List[Dict[str, Any]], **kwargs) -> "ExecutionResult":
        return cls(status=ExecutionStatus.FAILED, engine_name=engine, errors=errors, **kwargs)

from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

# Bounds on attachment lists so an unbounded JSON body can't exhaust memory
# before per-attachment size caps apply.
_MAX_ATTACHMENTS = 5

# Per-attachment payload caps: images arrive as base64 (~1.37x binary size) and
# files as extracted text. They bound the worst-case vision/prompt token cost of
# a single chat turn without affecting normal text-only conversations.
_MAX_IMAGE_B64_CHARS = 1_600_000    # ~1.2 MB binary per image
_MAX_FILE_CONTENT_CHARS = 200_000   # ~200 KB of text per file


def _bounded_list(v, default=None):
    if v is None:
        return default
    if len(v) > _MAX_ATTACHMENTS:
        raise ValueError(f"A maximum of {_MAX_ATTACHMENTS} attachments are allowed.")
    return v


def _validate_attachment_sizes(images=None, files=None):
    """Raise when any single attachment exceeds its per-item payload cap."""
    for i, img in enumerate(images or [], start=1):
        if not isinstance(img, str) or len(img) > _MAX_IMAGE_B64_CHARS:
            raise ValueError(f"Image {i} exceeds the maximum allowed size.")
    for i, file in enumerate(files or [], start=1):
        content = (file or {}).get("content") or ""
        if len(content) > _MAX_FILE_CONTENT_CHARS:
            raise ValueError(f"File {i} exceeds the maximum allowed size.")

class ChatRequest(BaseModel):
    """Standard inbound payload for Chat API."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    conversation_id: Optional[str] = None
    message: Optional[str] = None
    query: Optional[str] = None
    stream: bool = False
    language: Optional[str] = None
    images: Optional[List[str]] = Field(default=None, max_length=_MAX_ATTACHMENTS)
    files: Optional[List[Dict[str, Any]]] = Field(default=None, max_length=_MAX_ATTACHMENTS)
    token: Optional[str] = None
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    client_id: Optional[str] = None

    @field_validator("images", "files")
    @classmethod
    def cap_attachments(cls, v):
        return _bounded_list(v)

    @model_validator(mode="after")
    @classmethod
    def validate_attachment_sizes(cls, m: "ChatRequest") -> "ChatRequest":
        _validate_attachment_sizes(images=m.images, files=m.files)
        return m

    @model_validator(mode="before")
    @classmethod
    def map_query_and_message(cls, data: Any) -> Any:
        if isinstance(data, dict):
            q = data.get("query")
            m = data.get("message")
            if q and not m:
                data["message"] = q
            elif m and not q:
                data["query"] = m

            # Ensure at least one is provided
            if not data.get("message") and not data.get("query"):
                raise ValueError("Either 'message' or 'query' must be provided")
        return data

class ChatResponse(BaseModel):
    """Standard outbound payload for Chat API."""
    model_config = ConfigDict(arbitrary_types_allowed=True)
    conversation_id: str
    message: str
    query: Optional[str] = None # Added for compatibility
    answer: Optional[str] = None # Added for compatibility
    metadata: Dict[str, Any] = Field(default_factory=dict)
    used_tools: List[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def map_message_and_answer(cls, data: Any) -> Any:
        if isinstance(data, dict):
            m = data.get("message")
            a = data.get("answer")
            if m and not a:
                data["answer"] = m
            elif a and not m:
                data["message"] = a
        return data

from app.platform.models import UserProfile, Course, Progress, Recommendation, Certificate

class PlatformContextPayload(BaseModel):
    profile: Optional[UserProfile] = None
    courses: List[Course] = []
    progress: List[Progress] = []
    recommendations: List[Recommendation] = []
    certificates: List[Certificate] = []

class SessionInitializationResponse(BaseModel):
    welcome_message: str
    platform_context: PlatformContextPayload
