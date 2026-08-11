from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.services.lab.models import MistakeCategory
from typing import Any

class MistakeDetectionTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="mistake_detection",
            metadata=ToolMetadata(
                input_schema={"action": "str"},
                output_schema={"blocker": "str", "category": "MistakeCategory"},
                tags=["lab", "mistake"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        action = kwargs.get("action", "").lower()
        if "flag" in action:
            return {"blocker": "Learner is attempting to brute force or guess the flag.", "category": MistakeCategory.WORKFLOW}
        if "stuck" in action:
            return {"blocker": "Learner is stuck and requires directional guidance.", "category": MistakeCategory.CONCEPT}
        if "syntax" in action or "error" in action:
            return {"blocker": "Learner encountered a syntax or tool error.", "category": MistakeCategory.SYNTAX}
        if "nmap" in action or "burp" in action:
            return {"blocker": "Learner might be using the tool incorrectly.", "category": MistakeCategory.TOOL_USAGE}
            
        return {"blocker": "No obvious blocker detected.", "category": MistakeCategory.UNKNOWN}
