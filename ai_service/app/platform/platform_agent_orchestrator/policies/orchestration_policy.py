from pydantic import BaseModel, Field
from typing import Dict, Any
from app.platform.platform_agent_orchestrator.policies.retry_policy import RetryPolicy
from app.platform.platform_agent_orchestrator.policies.aggregation_policy import AggregationPolicy
from app.platform.platform_agent_orchestrator.models import ExecutionStrategy

class OrchestrationPolicy(BaseModel):
    default_execution_strategy: ExecutionStrategy = ExecutionStrategy.HYBRID
    maximum_parallelism: int = 5
    maximum_workflow_depth: int = 10
    concurrency_limits: Dict[str, int] = Field(default_factory=dict)
    timeout_inheritance: bool = True
    retry_inheritance: bool = True
    default_retry_policy: RetryPolicy = Field(default_factory=RetryPolicy)
    default_aggregation_policy: AggregationPolicy = Field(default_factory=AggregationPolicy)
    execution_constraints: Dict[str, Any] = Field(default_factory=dict)
    resource_limits: Dict[str, Any] = Field(default_factory=dict)
