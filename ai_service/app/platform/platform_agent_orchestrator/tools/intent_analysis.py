from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.models import UserIntent, IntentType
from typing import Any

class IntentAnalysisTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="intent_analysis",
            metadata=ToolMetadata(
                input_schema={"request": "str"},
                output_schema={"intent": "UserIntent"},
                tags=["orchestration", "intent"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        request = kwargs.get("request", "")
        # Mock Logic for intent analysis
        # Uses standard prompt registry (mocked here)
        return UserIntent(
            intent_id="int-123",
            intent_type=IntentType.INVESTIGATION if "investigate" in request.lower() else IntentType.GENERAL_CHAT,
            confidence=0.95,
            requested_capabilities=["IOC_LOOKUP", "NETWORK_ANALYSIS"] if "investigate" in request.lower() else []
        )
