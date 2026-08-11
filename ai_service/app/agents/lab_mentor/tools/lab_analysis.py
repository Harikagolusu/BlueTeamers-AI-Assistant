from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.services.lab.models import LabState
from app.services.lab.state_machine import LabStateMachine
from typing import Any

class LabAnalysisTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="lab_analysis",
            metadata=ToolMetadata(
                input_schema={"lab_id": "str", "user_query": "str", "current_state": "LabState"},
                output_schema={"state": "LabState"},
                tags=["lab", "analysis"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        query = kwargs.get("user_query", "").lower()
        current_state = kwargs.get("current_state", LabState.NOT_STARTED)
        
        machine = LabStateMachine()
        machine.current_state = current_state
        
        if machine.is_terminal_state():
            return current_state

        next_state = current_state
        if "start" in query and machine.can_transition(LabState.INITIALIZING):
            next_state = LabState.INITIALIZING
        elif ("help" in query or "hint" in query) and machine.can_transition(LabState.AWAITING_HINT):
            next_state = LabState.AWAITING_HINT
        elif "flag" in query and machine.can_transition(LabState.IN_PROGRESS):
            next_state = LabState.IN_PROGRESS
        else:
            if current_state == LabState.INITIALIZING and machine.can_transition(LabState.IN_PROGRESS):
                next_state = LabState.IN_PROGRESS
                
        if next_state != current_state and machine.can_transition(next_state):
            machine.transition(next_state)
            
        return machine.current_state
