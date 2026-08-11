import logging
from typing import Any
from pydantic import BaseModel, Field, ValidationError
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.providers.threat_intelligence.base_provider import ThreatIntelligenceProvider

logger = logging.getLogger(__name__)

class ReputationInput(BaseModel):
    indicator: str = Field(..., description="The Indicator of Compromise to check reputation for")

class ReputationTool(BaseTool):
    """
    Analyzes risk and reputation of an indicator using a Threat Intelligence Provider.
    """
    def __init__(self, provider: ThreatIntelligenceProvider):
        super().__init__(
            name="reputation_tool",
            metadata=ToolMetadata(
                input_schema=ReputationInput.model_json_schema(),
                output_schema={
                    "type": "object",
                    "description": "Reputation and risk assessment"
                },
                capabilities=["threat_intelligence"]
            )
        )
        self._provider = provider

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        logger.info(f"Executing ReputationTool with args: {kwargs}")
        try:
            input_data = ReputationInput(**kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in ReputationTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        try:
            result = await self._provider.get_reputation(input_data.indicator)
            logger.debug(f"ReputationTool result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in ReputationTool execution: {e}")
            raise
