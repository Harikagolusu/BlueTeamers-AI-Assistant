from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from typing import Any

class MotivationCoachingTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="motivation_coaching",
            metadata=ToolMetadata(
                input_schema={"analytics": "LearningAnalytics", "patterns": "LearningPattern"},
                output_schema={"message": "str"},
                tags=["learning_coach", "motivation"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        # Mock logic
        return "You've been incredibly consistent this week. Mastering Nmap scanning will directly impact your SOC Analyst goal!"
