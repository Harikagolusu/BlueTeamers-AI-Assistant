from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.models import AggregatedResponse
from app.platform.platform_agent_orchestrator.policies.aggregation_policy import AggregationPolicy, AggregationStrategy
from typing import Any

class ResponseAggregationTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="response_aggregation",
            metadata=ToolMetadata(
                input_schema={"results": "list", "policy": "AggregationPolicy"},
                output_schema={"aggregated": "AggregatedResponse"},
                tags=["orchestration", "aggregation"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        results = kwargs.get("results", [])
        policy: AggregationPolicy = kwargs.get("policy", AggregationPolicy())
        
        summary = "Unified response generated successfully."
        sections = {}
        for res in results:
            sections[res.step_id] = str(res.output)
            
        return AggregatedResponse(
            summary=summary,
            detailed_sections=sections
        )
