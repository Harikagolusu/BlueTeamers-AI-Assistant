from pydantic import BaseModel, Field
from typing import List

class RetryPolicy(BaseModel):
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 30.0
    exponential_backoff: bool = True
    retryable_errors: List[str] = Field(default_factory=lambda: ["Timeout", "AgentUnavailable", "ExecutionError"])
    fallback_strategy: str = "GracefulDegradation"
