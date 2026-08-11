from pydantic import BaseModel
from typing import Dict, Any

class DelegationPolicy(BaseModel):
    max_delegation_depth: int = 3
    allow_recursive_delegation: bool = False

class CoordinationPolicy(BaseModel):
    parallel_execution_limit: int = 5
    require_consensus: bool = False
    consensus_strategy_name: str = "MAJORITY_VOTE"

class RetryPolicy(BaseModel):
    max_retries: int = 3
    backoff_factor: float = 2.0

class ConsensusPolicy(BaseModel):
    quorum_percentage: float = 0.51
    timeout_ms: int = 30000
