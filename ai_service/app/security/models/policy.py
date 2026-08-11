from pydantic import BaseModel, Field
from typing import Dict, Any, List

class PolicyRule(BaseModel):
    rule_id: str
    condition: str
    effect: str # "ALLOW" or "DENY"

class Policy(BaseModel):
    policy_id: str
    name: str
    resource_type: str
    rules: List[PolicyRule] = Field(default_factory=list)
