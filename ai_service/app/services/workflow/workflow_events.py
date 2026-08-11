from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from app.services.workflow.workflow_state import WorkflowState

class WorkflowEvent(BaseModel):
    workflow_id: str
    event_type: str
    state: WorkflowState
    timestamp: float = Field(default_factory=lambda: 0.0) # populated at creation
    details: Dict[str, Any] = Field(default_factory=dict)
