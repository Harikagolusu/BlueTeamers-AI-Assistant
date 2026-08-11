from app.tools.discovery.decorators.tool_decorator import tool
import re
from typing import Any
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext

@tool(name="IOCExtractorTool", description="Executes IOCExtractorTool")
class IOCExtractorTool(BaseTool):
    """
    Extracts Indicators of Compromise (IPs, hashes, domains) from raw text.
    """
    def __init__(self):
        super().__init__(
            name="IOCExtractorTool",
            metadata=ToolMetadata(
                input_schema={"text": "string"},
                output_schema={"ips": "list", "hashes": "list", "domains": "list"},
                capabilities=["LOG_ANALYSIS", "INVESTIGATION"],
                tags=["ioc", "regex"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        text = kwargs.get("text", "")
        
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        hash_pattern = r'\b[a-fA-F0-9]{32,64}\b'
        domain_pattern = r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        
        ips = re.findall(ip_pattern, text)
        hashes = re.findall(hash_pattern, text)
        domains = re.findall(domain_pattern, text)
        
        return {
            "ips": list(set(ips)),
            "hashes": list(set(hashes)),
            "domains": list(set(domains))
        }
