import logging
from typing import Any, List
from pydantic import BaseModel, Field, ValidationError
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.providers.threat_intelligence.base_provider import ThreatIntelligenceProvider

logger = logging.getLogger(__name__)

class IndicatorCorrelationInput(BaseModel):
    indicators: List[str] = Field(..., description="List of indicators to correlate")

class IndicatorCorrelationTool(BaseTool):
    """
    Correlates multiple indicators to find relationships using a Threat Intelligence Provider.
    """
    def __init__(self, provider: ThreatIntelligenceProvider):
        super().__init__(
            name="indicator_correlation_tool",
            metadata=ToolMetadata(
                input_schema=IndicatorCorrelationInput.model_json_schema(),
                output_schema={
                    "type": "object",
                    "description": "Correlation results including relationships and possible campaigns/actors"
                },
                capabilities=["threat_intelligence"]
            )
        )
        self._provider = provider

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        logger.info(f"Executing IndicatorCorrelationTool with args: {kwargs}")
        try:
            input_data = IndicatorCorrelationInput(**kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in IndicatorCorrelationTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        try:
            result = await self._provider.correlate_indicators(input_data.indicators)
            logger.debug(f"IndicatorCorrelationTool result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in IndicatorCorrelationTool execution: {e}")
            raise
