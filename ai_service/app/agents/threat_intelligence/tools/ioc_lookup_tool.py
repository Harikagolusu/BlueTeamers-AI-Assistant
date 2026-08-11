import logging
from typing import Any
from pydantic import BaseModel, Field, ValidationError
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.providers.threat_intelligence.base_provider import ThreatIntelligenceProvider

logger = logging.getLogger(__name__)

class IOCLookupInput(BaseModel):
    indicator: str = Field(..., description="The Indicator of Compromise (IP, Domain, Hash, URL) to lookup")

class IOCLookupTool(BaseTool):
    """
    Looks up Indicators of Compromise (IP, Domain, Hash, URL) using a Threat Intelligence Provider.
    """
    def __init__(self, provider: ThreatIntelligenceProvider):
        super().__init__(
            name="ioc_lookup_tool",
            metadata=ToolMetadata(
                input_schema=IOCLookupInput.model_json_schema(),
                output_schema={
                    "type": "object",
                    "description": "Details about the IOC"
                },
                capabilities=["threat_intelligence"]
            )
        )
        self._provider = provider

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        logger.info(f"Executing IOCLookupTool with args: {kwargs}")
        try:
            input_data = IOCLookupInput(**kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in IOCLookupTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        try:
            result = await self._provider.lookup_ioc(input_data.indicator)
            logger.debug(f"IOCLookupTool result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in IOCLookupTool execution: {e}")
            raise

