from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.policies.failure_classifier import FailureClassifier
from typing import Any

class FailureRecoveryTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="failure_recovery",
            metadata=ToolMetadata(
                input_schema={"error": "Any", "retry_policy": "RetryPolicy"},
                output_schema={"action": "str"},
                tags=["orchestration", "recovery"]
            )
        )

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        error = kwargs.get("error")
        policy = kwargs.get("retry_policy")
        
        category = FailureClassifier.classify(error)
        
        if category.value in policy.retryable_errors:
            return "RETRY"
        return "FALLBACK"
