import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext

logger = logging.getLogger(__name__)

class InvestigationPlanningInput(BaseModel):
    evidence_types: List[str] = Field(..., description="List of evidence types collected")

class InvestigationPlanningTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="investigation_planning_tool",
            description="Determines investigation sequence and required expert agents.",
            capabilities=["planning"],
            tags=["investigation"]
        )
        super().__init__(name="investigation_planning_tool", metadata=metadata)

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        try:
            validated = InvestigationPlanningInput(**kwargs)
        except Exception as e:
            logger.error(f"Validation error in InvestigationPlanningTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        # Basic planning logic based on evidence types
        required_agents = []
        if any(t in str(validated.evidence_types).lower() for t in ["log", "alert", "sysmon"]):
            required_agents.append("soc_analyst")
        if any(t in str(validated.evidence_types).lower() for t in ["ioc", "hash", "ip", "domain", "url"]):
            required_agents.append("threat_intelligence")

        # If nothing specifically triggered, default to both for comprehensive analysis
        if not required_agents:
            required_agents = ["soc_analyst", "threat_intelligence"]

        plan = {
            "investigation_steps": [
                "1. Normalize evidence.",
                "2. Perform primary correlation.",
                f"3. Invoke {', '.join(required_agents)} for expert analysis.",
                "4. Aggregate findings.",
                "5. Generate incident timeline.",
                "6. Produce final executive summary."
            ],
            "required_expert_agents": required_agents,
            "required_tools": [
                "evidence_collection_tool",
                "evidence_correlation_tool",
                "incident_timeline_tool",
                "investigation_summary_tool"
            ],
            "confidence_score": 95
        }
        logger.info(f"Generated investigation plan requiring {required_agents}.")
        return plan
