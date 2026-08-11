from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.services.lab.models import MentorFeedback
from typing import Any

class LabPlanningTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="lab_planning",
            metadata=ToolMetadata(
                input_schema={"history": "AttemptHistory", "state": "LabState"},
                output_schema={"feedback": "MentorFeedback"},
                tags=["lab", "planning"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        return MentorFeedback(
            positive_reinforcement="Good job getting this far!",
            observed_strengths=["Persistence"],
            observed_weaknesses=[],
            recommended_next_action="Continue mapping the target network.",
            confidence=0.9
        )
