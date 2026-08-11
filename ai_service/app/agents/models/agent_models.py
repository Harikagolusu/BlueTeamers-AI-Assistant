from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.planning.models.plan import ExecutionPlan, ExecutionStep
from app.runtime.models.context import TokenUsage, CostAggregation

class AgentState(str, Enum):
    IDLE = "IDLE"
    PLANNING = "PLANNING"
    RETRIEVING = "RETRIEVING"
    EXECUTING = "EXECUTING"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class AgentCapability(str, Enum):
    INVESTIGATION = "INVESTIGATION"
    MITRE_MAPPING = "MITRE_MAPPING"
    LOG_ANALYSIS = "LOG_ANALYSIS"
    TIMELINE_GENERATION = "TIMELINE_GENERATION"
    REPORTING = "REPORTING"
    THREAT_INTEL = "THREAT_INTEL"

class AgentResult(BaseModel):
    success: bool
    response: str
    confidence: float = 0.0
    citations: List[str] = Field(default_factory=list)
    tools_used: List[str] = Field(default_factory=list)
    execution_time: float = 0.0
    memory_updates: int = 0
    events: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    cost: CostAggregation = Field(default_factory=CostAggregation)
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)

class StepExecution(BaseModel):
    step_id: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    success: bool = False
    output: Any = None
    error: Optional[str] = None
    retries: int = 0
