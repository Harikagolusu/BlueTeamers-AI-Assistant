import logging
from typing import Any
from pydantic import BaseModel, Field, ValidationError
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.providers.threat_intelligence.base_provider import ThreatIntelligenceProvider

logger = logging.getLogger(__name__)

class MITREMappingInput(BaseModel):
    entity: str = Field(..., description="The entity (technique ID, threat actor, or campaign) to map")

class MITREMappingTool(BaseTool):
    """
    Maps indicators or entities to MITRE ATT&CK techniques using a Threat Intelligence Provider.
    """
    def __init__(self, provider: ThreatIntelligenceProvider):
        super().__init__(
            name="mitre_mapping_tool",
            metadata=ToolMetadata(
                input_schema=MITREMappingInput.model_json_schema(),
                output_schema={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "description": "MITRE ATT&CK technique details"
                    },
                    "description": "List of mapped techniques"
                },
                capabilities=["threat_intelligence"]
            )
        )
        self._provider = provider

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        logger.info(f"Executing MITREMappingTool with args: {kwargs}")
        try:
            input_data = MITREMappingInput(**kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in MITREMappingTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        try:
            result = await self._provider.map_to_mitre(input_data.entity)
            logger.debug(f"MITREMappingTool result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in MITREMappingTool execution: {e}")
            raise
