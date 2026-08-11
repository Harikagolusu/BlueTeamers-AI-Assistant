import uuid
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.planning.models.plan import ExecutionPlan
from app.models.chat.chat_models import ExecutionResult

class CoordinationState(str, Enum):
    PENDING = "PENDING"
    ROUTING = "ROUTING"
    EXECUTING = "EXECUTING"
    AGGREGATING = "AGGREGATING"
    CONSENSUS = "CONSENSUS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AgentTask(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    step_id: str
    assigned_agent_id: str
    status: CoordinationState = CoordinationState.PENDING
    result: Optional[ExecutionResult] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None

class AgentExecutionResult(BaseModel):
    task_id: str
    success: bool
    result: ExecutionResult
    metrics: Dict[str, Any] = Field(default_factory=dict)
    
class MultiAgentExecutionPlan(BaseModel):
    """
    Composes the original ExecutionPlan and adds multi-agent orchestration metadata.
    """
    multi_plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_execution_plan: ExecutionPlan
    
    delegated_tasks: List[AgentTask] = Field(default_factory=list)
    dependencies: Dict[str, List[str]] = Field(default_factory=dict) # task_id -> [dependent_task_ids]
    routing_metadata: Dict[str, Any] = Field(default_factory=dict)
    coordination_policy: Dict[str, Any] = Field(default_factory=dict)
    execution_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    state: CoordinationState = CoordinationState.PENDING
