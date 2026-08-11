from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid

class BaseRuntimeContext(BaseModel):
    """
    Foundational context for all distributed runtime components.
    Ensures strict propagation of tracing and isolation boundaries.
    """
    trace_id: str = Field(default_factory=lambda: f"trace-{uuid.uuid4().hex[:8]}")
    correlation_id: str = Field(default_factory=lambda: f"corr-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    session_id: str = "default_session"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class WorkflowContext(BaseRuntimeContext):
    """Context for a specific workflow execution."""
    workflow_id: str
    execution_strategy: str = "SEQUENTIAL"

class ExecutionContext(BaseRuntimeContext):
    """Context for an individual step/capability execution."""
    execution_id: str
    step_id: str
    target_agent: Optional[str] = None

class AgentContext(BaseRuntimeContext):
    """Context passed explicitly to an agent."""
    agent_id: str
    capabilities: list = Field(default_factory=list)

class MemoryContext(BaseRuntimeContext):
    """Context for persistence boundaries."""
    append_only: bool = True
    history_level: str = "full"

class StreamingContext(BaseRuntimeContext):
    """Context for the streaming pipeline."""
    chunk_size: int = 1024
    flush_interval: float = 0.5
