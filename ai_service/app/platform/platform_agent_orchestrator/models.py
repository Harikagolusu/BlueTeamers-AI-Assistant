from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from app.platform.platform_agent_orchestrator.policies.retry_policy import RetryPolicy
from app.platform.platform_agent_orchestrator.repositories.agent_health import AgentHealth

class IntentType(str, Enum):
    INVESTIGATION = "INVESTIGATION"
    EDUCATION = "EDUCATION"
    HYBRID = "HYBRID"
    THREAT_ANALYSIS = "THREAT_ANALYSIS"
    GENERAL_CHAT = "GENERAL_CHAT"
    UNKNOWN = "UNKNOWN"

class ExecutionStrategy(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    HYBRID = "HYBRID"
    DYNAMIC = "DYNAMIC"

class ExecutionState(str, Enum):
    # Legacy states
    PENDING = "PENDING"
    
    # Phase 4 Strict Runtime States
    CREATED = "CREATED"
    READY = "READY"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    RETRYING = "RETRYING"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    SKIPPED = "SKIPPED"

class UserIntent(BaseModel):
    intent_id: str
    intent_type: IntentType
    confidence: float
    requested_capabilities: List[str] = Field(default_factory=list)
    execution_priority: int = 1
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ExecutionStep(BaseModel):
    step_id: str
    capability: str
    target_agent: Optional[str] = None
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    timeout: float = 30.0
    retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)
    execution_order: int
    state: ExecutionState = ExecutionState.PENDING
    dependencies: List[str] = Field(default_factory=list)

class ExecutionPlan(BaseModel):
    plan_id: str
    goal: str
    execution_steps: List[ExecutionStep] = Field(default_factory=list)
    dependencies: Dict[str, List[str]] = Field(default_factory=dict)
    parallel_groups: List[List[str]] = Field(default_factory=list)
    estimated_duration: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    strategy: ExecutionStrategy = ExecutionStrategy.SEQUENTIAL

class AgentInvocation(BaseModel):
    invocation_id: str
    agent_name: str
    capability: str
    payload: Dict[str, Any]
    timeout: float
    retry_count: int = 0
    execution_time: float = 0.0

class ExecutionResult(BaseModel):
    step_id: str
    success: bool
    output: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    latency: float = 0.0
    retry_count: int = 0
    trace_id: Optional[str] = None
    telemetry: Dict[str, Any] = Field(default_factory=dict)

class ExecutionWave(BaseModel):
    wave_id: str
    steps: List[ExecutionStep] = Field(default_factory=list)

class ExecutionSchedule(BaseModel):
    schedule_id: str
    plan_id: str
    waves: List[ExecutionWave] = Field(default_factory=list)

class ExecutionBatch(BaseModel):
    batch_id: str
    invocations: List[AgentInvocation] = Field(default_factory=list)

class ExecutionQueue(BaseModel):
    queue_id: str
    pending_batches: List[ExecutionBatch] = Field(default_factory=list)

class AggregatedResponse(BaseModel):
    summary: str
    detailed_sections: Dict[str, str] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)
    execution_metrics: Dict[str, Any] = Field(default_factory=dict)

class ConversationContext(BaseModel):
    history: List[Dict[str, str]] = Field(default_factory=list)
    user_profile: Dict[str, Any] = Field(default_factory=dict)

class SharedExecutionState(BaseModel):
    memory: Dict[str, Any] = Field(default_factory=dict)

class ExecutionMetadata(BaseModel):
    workflow_id: str
    request_id: str
    metrics: Dict[str, Any] = Field(default_factory=dict)

class ExecutionContext(BaseModel):
    request_id: str
    workflow_id: str
    execution_plan: Optional[ExecutionPlan] = None
    execution_schedule: Optional[ExecutionSchedule] = None
    queue: Optional[ExecutionQueue] = None
    active_steps: List[str] = Field(default_factory=list)
    completed_steps: List[str] = Field(default_factory=list)
    failed_steps: List[str] = Field(default_factory=list)
    pending_steps: List[str] = Field(default_factory=list)
    retry_history: Dict[str, int] = Field(default_factory=dict)
    shared_memory: SharedExecutionState = Field(default_factory=SharedExecutionState)

class OrchestratorContext(BaseModel):
    conversation: ConversationContext = Field(default_factory=ConversationContext)
    execution: ExecutionContext
    metadata: ExecutionMetadata
    active_workflow: Optional[str] = None
