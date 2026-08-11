from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class WorkflowContext(BaseModel):
    """
    Shared state container passed across workflow steps.
    """
    workflow_id: str
    session_id: str
    global_state: Dict[str, Any] = Field(default_factory=dict)
    step_outputs: Dict[str, Any] = Field(default_factory=dict)

    def set_state(self, key: str, value: Any) -> None:
        self.global_state[key] = value
        
    def get_state(self, key: str, default: Any = None) -> Any:
        return self.global_state.get(key, default)
        
    def set_step_output(self, step_name: str, value: Any) -> None:
        self.step_outputs[step_name] = value
        
    def get_step_output(self, step_name: str) -> Any:
        return self.step_outputs.get(step_name)
