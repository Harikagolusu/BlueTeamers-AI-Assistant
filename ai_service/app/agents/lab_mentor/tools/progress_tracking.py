from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.services.lab.models import AttemptHistory, MentoringMetrics
from typing import Any
import datetime
from datetime import timezone

class ProgressTrackingTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="progress_tracking",
            metadata=ToolMetadata(
                input_schema={"history": "AttemptHistory", "metrics": "MentoringMetrics", "action": "str"},
                output_schema={"history": "AttemptHistory", "metrics": "MentoringMetrics"},
                tags=["lab", "progress"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        history = kwargs.get("history")
        if not history:
            history = AttemptHistory()
            
        metrics = kwargs.get("metrics")
        if not metrics:
            metrics = MentoringMetrics()
            
        action = kwargs.get("action", "").lower()
        
        # Track time implicitly (assuming 60s per turn for mock)
        history.time_on_current_step += 60
        history.total_time_spent += 60
        history.last_progress_timestamp = datetime.datetime.now(timezone.utc)

        if "hint" in action:
            history.hint_requests += 1
            metrics.hints_generated += 1
        elif "flag" in action:
            history.retry_count += 1
            
        if action == history.model_dump().get("last_action", "") and "flag" in action:
            history.repeated_mistakes += 1
            
        # Update metrics derived values
        if history.retry_count > 0:
            metrics.retry_rate = history.repeated_mistakes / history.retry_count
            
        return {"history": history, "metrics": metrics}
