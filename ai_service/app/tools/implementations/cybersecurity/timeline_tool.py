from app.tools.discovery.decorators.tool_decorator import tool
from typing import Any
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext

@tool(name="TimelineTool", description="Executes TimelineTool")
class TimelineTool(BaseTool):
    """
    Sorts unstructured events chronologically.
    """
    def __init__(self):
        super().__init__(
            name="TimelineTool",
            metadata=ToolMetadata(
                input_schema={"events": "list"},
                output_schema={"timeline": "list"},
                capabilities=["TIMELINE_GENERATION"],
                tags=["timeline"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        events = kwargs.get("events", [])
        if not isinstance(events, list):
            return {"error": "events must be a list of dictionaries containing 'timestamp'"}
            
        try:
            sorted_events = sorted(events, key=lambda x: x.get("timestamp", ""))
            return {"timeline": sorted_events}
        except Exception as e:
            return {"error": f"Failed to sort events: {str(e)}"}
