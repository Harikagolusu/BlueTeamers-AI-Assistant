import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field

from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.agents.investigation.models import Timeline, TimelineEvent

logger = logging.getLogger(__name__)

class IncidentTimelineInput(BaseModel):
    correlated_data: Dict[str, Any] = Field(..., description="Data from correlation and expert agents")

class IncidentTimelineTool(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="incident_timeline_tool",
            description="Generates MITRE ATT&CK ordered timeline.",
            capabilities=["timeline_generation"],
            tags=["investigation"]
        )
        super().__init__(name="incident_timeline_tool", metadata=metadata)

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        try:
            validated = IncidentTimelineInput(**kwargs)
        except Exception as e:
            logger.error(f"Validation error in IncidentTimelineTool: {e}")
            raise ValueError(f"Invalid input: {e}")

        # Create a mock sorted timeline representing the MITRE killchain progression
        # In a real scenario, this would parse real timestamps and map them.
        events = [
            TimelineEvent(
                timestamp="T00:00:00",
                event_type="Initial Access",
                description="Suspicious entry point identified.",
                mitre_tactic="Initial Access",
                mitre_technique="T1190"
            ),
            TimelineEvent(
                timestamp="T00:10:00",
                event_type="Execution",
                description="Malicious payload executed.",
                mitre_tactic="Execution",
                mitre_technique="T1059"
            ),
            TimelineEvent(
                timestamp="T00:15:00",
                event_type="Persistence",
                description="Registry key modified for persistence.",
                mitre_tactic="Persistence",
                mitre_technique="T1547"
            )
        ]
        
        timeline = Timeline(events=events)
        logger.info("Generated incident timeline mapped to MITRE ATT&CK.")
        return timeline.model_dump()
