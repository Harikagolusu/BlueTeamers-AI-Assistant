from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from app.planning.models.plan import ExecutionPlan

class PlanningContext(BaseModel):
    """
    Wrapper for planning output to keep context metadata organized.
    """
    plan: Optional[ExecutionPlan] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    estimates: Dict[str, Any] = Field(default_factory=dict)
    validation_results: List[str] = Field(default_factory=list)
