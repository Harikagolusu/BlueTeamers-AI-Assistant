from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, ConfigDict

class ExecutionContext(BaseModel):
    """
    Highly structured, immutable context passed throughout the execution pipeline.
    Solves prop-drilling and ensures metadata travels universally.
    """
    correlation_id: UUID = Field(default_factory=uuid4, description="Correlation ID for the entire request")
    trace_id: UUID = Field(default_factory=uuid4, description="Trace ID for OpenTelemetry spans")
    session_user: Optional[str] = Field(default=None, description="Authenticated user ID")
    tenant_id: Optional[str] = Field(default=None, description="Tenant ID for isolation")
    
    # In a real app, memory could be a distinct object. For now, we type it broadly.
    memory: Dict[str, Any] = Field(default_factory=dict, description="Conversational context/history")
    
    permissions: Dict[str, bool] = Field(default_factory=dict, description="RBAC permissions mapping")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata injected by enrichment")
    feature_flags: Dict[str, bool] = Field(default_factory=dict, description="Feature flag evaluations")
    config: Dict[str, Any] = Field(default_factory=dict, description="Environment or tenant configuration overrides")
    
    streaming_mode: bool = Field(default=False, description="Flag indicating if the client expects an SSE stream")
    
    # In a pure async system, cancellation tokens are often managed via asyncio.Task,
    # but we can pass a boolean flag reference or specific token object here.
    cancellation_requested: bool = Field(default=False, description="Flag indicating if request was cancelled")
    
    # Enforce immutability. To change state, a new copy must be derived.
    model_config = ConfigDict(frozen=True)

    def with_memory(self, memory: Dict[str, Any]) -> "ExecutionContext":
        """Returns a new context with updated memory."""
        return self.model_copy(update={"memory": memory})

    def request_cancellation(self) -> "ExecutionContext":
        """Returns a new context with cancellation requested."""
        return self.model_copy(update={"cancellation_requested": True})
