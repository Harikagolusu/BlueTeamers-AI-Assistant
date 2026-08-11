from pydantic import BaseModel, Field
from typing import List

class SecurityPolicy(BaseModel):
    max_memory_mb: int = 256
    max_execution_time_ms: int = 5000
    allowed_builtins: List[str] = Field(default_factory=lambda: ["json", "datetime", "math"])
    network_egress_allowed: bool = False
