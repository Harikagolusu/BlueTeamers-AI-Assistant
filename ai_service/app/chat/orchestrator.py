from typing import List
from app.chat.interfaces.i_chat_orchestrator import IChatOrchestrator
from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.chat.exceptions.chat_exceptions import RoutingError

class ChatOrchestrator(IChatOrchestrator):
    """
    Executes a sequence of pluggable stages to fulfill a chat request.
    """
    def __init__(self, stages: List[IExecutionStage]):
        self._stages = stages

    async def execute_pipeline(self, context: ExecutionContext) -> ExecutionResult:
        current_context = context
        
        for stage in self._stages:
            # Pass the immutable context into the stage and get a new one out
            current_context = await stage.execute(current_context)
            
            # Check for cancellation
            if current_context.cancellation_requested:
                break
                
        # Extract the final result from context metadata
        result = current_context.metadata.get("execution_result")
        if not result:
            # Fallback if no result was produced
            result = ExecutionResult.failed(
                engine="Orchestrator",
                errors=[{"error": "Pipeline completed without generating a result."}]
            )
            
        return result
