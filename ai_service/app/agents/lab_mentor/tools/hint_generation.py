from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.services.lab.models import Hint, HintLevel
from typing import Any

class HintGenerationTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="hint_generation",
            metadata=ToolMetadata(
                input_schema={"blocker": "str", "level": "HintLevel"},
                output_schema={"hint": "Hint"},
                tags=["lab", "hint"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        level = kwargs.get("level", HintLevel.LEVEL_1)
        blocker = kwargs.get("blocker", "")
        
        # Mock logic based on hint level
        if level == HintLevel.LEVEL_1:
            content = "Consider the fundamental concepts related to this step."
        elif level == HintLevel.LEVEL_2:
            content = "Look closer at the specific headers or parameters you are sending."
        else:
            content = "Try using a specific tool like Nmap or Burp to analyze the exact response."
            
        return Hint(level=level, content=content, reasoning=f"Generated for blocker: {blocker}", is_safe=True)
