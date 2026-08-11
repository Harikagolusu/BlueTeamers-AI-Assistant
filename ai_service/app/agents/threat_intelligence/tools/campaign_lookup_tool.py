import logging
from typing import Any
from pydantic import BaseModel, Field, ValidationError
from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.providers.threat_intelligence.base_provider import ThreatIntelligenceProvider

logger = logging.getLogger(__name__)

class CampaignLookupInput(BaseModel):
    campaign_name: str = Field(..., description="The name of the campaign")

class CampaignLookupTool(BaseTool):
    """
    Looks up known campaigns using a Threat Intelligence Provider.
    """
    def __init__(self, provider: ThreatIntelligenceProvider):
        super().__init__(
            name="campaign_lookup_tool",
            metadata=ToolMetadata(
                input_schema=CampaignLookupInput.model_json_schema(),
                output_schema={
                    "type": "object",
                    "description": "Details about the campaign"
                },
                capabilities=["threat_intelligence"]
            )
        )
        self._provider = provider

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        logger.info(f"Executing CampaignLookupTool with args: {kwargs}")
        try:
            input_data = CampaignLookupInput(**kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in CampaignLookupTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        try:
            result = await self._provider.get_campaign(input_data.campaign_name)
            logger.debug(f"CampaignLookupTool result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in CampaignLookupTool execution: {e}")
            raise
