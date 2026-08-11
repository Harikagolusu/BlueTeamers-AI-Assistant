from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class WorkflowEvaluation(BaseModel):
    workflow_id: str
    total_latency_ms: float = 0.0
    total_cost: float = 0.0
    overall_success: bool
    steps_evaluated: int = 0
    anomalies_detected: List[str] = Field(default_factory=list)
    
class CapabilityEvaluation(BaseModel):
    capability: str
    resolved_provider: str
    routing_latency_ms: float
    fallback_used: bool = False
    
class ToolEvaluation(BaseModel):
    tool_name: str
    success: bool
    latency_ms: float
    retries_used: int = 0
    errors: List[str] = Field(default_factory=list)

class ExecutionEvaluation(BaseModel):
    execution_id: str
    agent_name: str
    workflow_eval: Optional[WorkflowEvaluation] = None
    capability_evals: List[CapabilityEvaluation] = Field(default_factory=list)
    tool_evals: List[ToolEvaluation] = Field(default_factory=list)
    recovery_successful: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
