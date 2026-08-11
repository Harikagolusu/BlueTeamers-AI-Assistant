from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional
import uuid

class Capability(str, Enum):
    LLM = "LLM"
    RAG = "RAG"
    TOOL = "TOOL"
    MEMORY = "MEMORY"
    SEARCH = "SEARCH"
    REASONING = "REASONING"
    CLARIFICATION = "CLARIFICATION"
    KNOWLEDGE_ASSISTANT = "KNOWLEDGE_ASSISTANT"
    INVESTIGATION_AGENT = "INVESTIGATION_AGENT"
    LEARNING_COACH = "LEARNING_COACH"
    AGGREGATOR = "AGGREGATOR"

class ExecutionPlanStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    READY = "READY"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class ExecutionStrategy(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    CONDITIONAL = "CONDITIONAL"
    FALLBACK = "FALLBACK"
    CLARIFICATION = "CLARIFICATION"
    DEFERRED = "DEFERRED"

class ExecutionConstraint(BaseModel):
    max_cost: float = 0.0
    max_tokens: int = 0
    timeout_seconds: float = 0.0

class ExecutionStep(BaseModel):
    step_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    required_capability: Capability
    expected_input: Dict[str, Any] = Field(default_factory=dict)
    expected_output: str = ""
    dependencies: List[str] = Field(default_factory=list) # List of step_ids
    retry_policy: Dict[str, Any] = Field(default_factory=dict)
    timeout: float = 30.0
    optional: bool = False

class ExecutionPlan(BaseModel):
    model_config = ConfigDict(frozen=True)

    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    goal: str
    priority: int = 1
    execution_strategy: ExecutionStrategy = ExecutionStrategy.SEQUENTIAL
    estimated_cost: float = 0.0
    estimated_tokens: int = 0
    estimated_time_ms: float = 0.0
    steps: List[ExecutionStep] = Field(default_factory=list)
    capabilities_required: List[Capability] = Field(default_factory=list)
    success_criteria: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: ExecutionPlanStatus = ExecutionPlanStatus.DRAFT
