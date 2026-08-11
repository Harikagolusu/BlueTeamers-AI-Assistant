import logging
from typing import Any
from pydantic import BaseModel, Field, ValidationError
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.providers.threat_intelligence.base_provider import ThreatIntelligenceProvider

logger = logging.getLogger(__name__)

class ThreatActorInput(BaseModel):
    actor_name: str = Field(..., description="The name of the threat actor")

class ThreatActorTool(BaseTool):
    """
    Looks up known threat actors and their TTPs using a Threat Intelligence Provider.
    """
    def __init__(self, provider: ThreatIntelligenceProvider):
        super().__init__(
            name="threat_actor_tool",
            metadata=ToolMetadata(
                input_schema=ThreatActorInput.model_json_schema(),
                output_schema={
                    "type": "object",
                    "description": "Details about the threat actor"
                },
                capabilities=["threat_intelligence"]
            )
        )
        self._provider = provider

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        logger.info(f"Executing ThreatActorTool with args: {kwargs}")
        try:
            input_data = ThreatActorInput(**kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in ThreatActorTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        try:
            result = await self._provider.get_threat_actor(input_data.actor_name)
            logger.debug(f"ThreatActorTool result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in ThreatActorTool execution: {e}")
            raise
