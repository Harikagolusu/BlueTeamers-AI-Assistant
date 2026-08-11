from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.agents.assessment_coach.models import CompetencyGap, CompetencyCategory
from typing import Any

class GapAnalysisTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="gap_analysis",
            metadata=ToolMetadata(
                input_schema={"learner_id": "str", "competency_profile": "dict"},
                output_schema={"gaps": "list"},
                tags=["assessment_coach", "gap_analysis", "evaluation"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        return [
            CompetencyGap(
                category=CompetencyCategory.PRACTICAL_SKILLS,
                current_score=5.0,
                target_score=8.0,
                description="Needs improvement in log analysis.",
                severity="HIGH",
                business_impact="Slower incident triage times.",
                prerequisite_dependency="Basic Networking",
                recommended_remediation="Complete the Advanced Log Analysis module."
            )
        ]
