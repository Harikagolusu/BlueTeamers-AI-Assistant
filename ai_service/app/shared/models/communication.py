from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.services.capabilities.capability import Capability

class AgentMetadata(BaseModel):
    agent_id: str
    name: str
    version: str
    capabilities: List[Capability] = Field(default_factory=list)
    owner: str = "system"

class AgentRequest(BaseModel):
    request_id: str
    session_id: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentExecutionContext(BaseModel):
    execution_id: str
    session_id: str
    workflow_id: Optional[str] = None
    parent_execution_id: Optional[str] = None
    state: Dict[str, Any] = Field(default_factory=dict)

class AgentExecutionMetrics(BaseModel):
    execution_time_ms: float = 0.0
    tokens_used: int = 0
    cost: float = 0.0
    tools_invoked: int = 0
    retries: int = 0

class AgentResponse(BaseModel):
    request_id: str
    success: bool
    data: Any = None
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class AgentExecutionResult(BaseModel):
    execution_id: str
    agent_name: str
    success: bool
    response: AgentResponse
    metrics: AgentExecutionMetrics = Field(default_factory=AgentExecutionMetrics)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AgentInvocation(BaseModel):
    invocation_id: str
    target_agent: Optional[str] = None
    target_capability: Optional[Capability] = None
    request: AgentRequest
    context: AgentExecutionContext
    timeout_seconds: int = 60
