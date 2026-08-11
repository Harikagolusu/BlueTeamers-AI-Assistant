from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.models import OrchestratorContext
from typing import Any

class MetricsCollectionTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="metrics_collection",
            metadata=ToolMetadata(
                input_schema={"orchestrator_context": "OrchestratorContext", "latency": "float", "step_name": "str"},
                output_schema={"success": "bool"},
                tags=["orchestration", "metrics"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        orch_context: OrchestratorContext = kwargs.get("orchestrator_context")
        latency = kwargs.get("latency", 0.0)
        step_name = kwargs.get("step_name", "unknown")
        
        # Track latencies in execution metadata
        orch_context.metadata.metrics[f"{step_name}_latency"] = latency
        return True
