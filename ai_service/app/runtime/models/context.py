from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    embedding_tokens: int = 0
    tool_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens + self.embedding_tokens + self.tool_tokens

class CostAggregation(BaseModel):
    llm_cost: float = 0.0
    embedding_cost: float = 0.0
    tool_cost: float = 0.0
    
    @property
    def total_cost(self) -> float:
        return self.llm_cost + self.embedding_cost + self.tool_cost

class RuntimeContext(BaseModel):
    """
    Operational state for a request. This is kept strictly separate from the conversational ExecutionContext.
    """
    trace_id: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    
    retry_count: int = 0
    latency_ms: float = 0.0
    
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    cost: CostAggregation = Field(default_factory=CostAggregation)
    
    cache_status: str = "MISS" # MISS, HIT, BYPASS
    quota_status: str = "OK" # OK, EXHAUSTED
    rate_limit_status: str = "OK" # OK, THROTTLED
    
    feature_flags: Dict[str, bool] = Field(default_factory=dict)
    diagnostics: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)
