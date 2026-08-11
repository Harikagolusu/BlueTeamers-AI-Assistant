from typing import Any
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext

from app.tools.discovery.decorators.tool_decorator import tool

@tool(name="IndicatorFetcherTool", description="Mocks an external Threat Intelligence integration (like VirusTotal).")
class IndicatorFetcherTool(BaseTool):
    """
    Mocks an external Threat Intelligence integration (like VirusTotal).
    """
    def __init__(self):
        super().__init__(
            name="IndicatorFetcherTool",
            metadata=ToolMetadata(
                input_schema={"indicator": "string", "type": "string"},
                output_schema={"malicious": "boolean", "reputation_score": "integer", "tags": "list"},
                capabilities=["THREAT_INTEL"],
                tags=["threat_intel", "vt"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        indicator = kwargs.get("indicator", "")
        
        # Mocks
        if indicator == "1.1.1.1":
            return {"malicious": False, "reputation_score": 100, "tags": ["dns", "cloudflare"]}
        if "evil" in indicator.lower() or indicator == "192.168.1.100":
            return {"malicious": True, "reputation_score": 5, "tags": ["c2", "malware", "suspicious"]}
            
        return {"malicious": False, "reputation_score": 50, "tags": ["unknown"]}
