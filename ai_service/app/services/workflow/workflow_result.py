from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.services.workflow.workflow_state import WorkflowState

class WorkflowResult(BaseModel):
    workflow_id: str
    success: bool
    state: WorkflowState
    output: Any = None
    errors: List[str] = Field(default_factory=list)
    execution_time: float = 0.0
