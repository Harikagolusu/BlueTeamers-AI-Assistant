import logging
from typing import Dict, Any
from pydantic import BaseModel, Field

from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.agents.investigation.models import InvestigationSummary

logger = logging.getLogger(__name__)

class InvestigationSummaryInput(BaseModel):
    investigation_context: Dict[str, Any] = Field(..., description="The complete aggregated investigation context")

class InvestigationSummaryTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="investigation_summary_tool",
            description="Generates Executive Summary, Evidence Summary, Timeline, Findings, MITRE Mapping, Recommendations, Confidence, and Next Steps.",
            capabilities=["summarization"],
            tags=["investigation"]
        )
        super().__init__(name="investigation_summary_tool", metadata=metadata)

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        try:
            validated = InvestigationSummaryInput(**kwargs)
        except Exception as e:
            logger.error(f"Validation error in InvestigationSummaryTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        # In a real tool, this would parse the complex context and generate a cohesive narrative.
        # Here we mock the generation for the architecture.
        summary = InvestigationSummary(
            executive_summary="The investigation analyzed multiple log sources and correlated them with CTI findings to identify a coordinated attack.",
            risk_assessment="HIGH. Critical assets have been exposed to known malicious entities.",
            affected_assets=["Workstation-01", "DomainController-Primary"],
            confidence=90
        )
        
        logger.info("Generated investigation summary.")
        return summary.model_dump()
