from app.tools.discovery.decorators.tool_decorator import tool
from typing import Any
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
import json

@tool(name="LogParserTool", description="Executes LogParserTool")
class LogParserTool(BaseTool):
    """
    Transforms unstructured or semi-structured log entries into normalized JSON.
    """
    def __init__(self):
        super().__init__(
            name="LogParserTool",
            metadata=ToolMetadata(
                input_schema={"raw_log": "string", "log_type": "string"},
                output_schema={"parsed_data": "dict"},
                capabilities=["LOG_ANALYSIS"],
                tags=["parser", "logs"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        raw_log = kwargs.get("raw_log", "")
        log_type = kwargs.get("log_type", "unknown").lower()
        
        # In a real implementation, this would use grok patterns or regex to parse lines.
        # Here we do a naive transform for demonstration.
        parsed = {"original": raw_log, "type": log_type}
        
        if "4625" in raw_log:
            parsed["event_id"] = 4625
            parsed["action"] = "Failed Logon"
            # Naive extraction for demo
            if "Administrator" in raw_log: parsed["target_user"] = "Administrator"
            
        elif "EncodedCommand" in raw_log:
            parsed["suspicious_flags"] = ["EncodedCommand"]
            parsed["process"] = "powershell.exe"
            
        return parsed
