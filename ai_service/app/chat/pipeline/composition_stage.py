from typing import Any
from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ChatResponse

class CompositionStage(IExecutionStage):
    """Converts the ExecutionResult into the final ChatResponse DTO or Stream."""
    
    @property
    def name(self) -> str:
        return "Composition"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        result = context.metadata.get("execution_result")
        
        if not result:
            return context
            
        metadata = {
            "latency": getattr(result, 'latency_ms', 0),
            "citations": getattr(result, 'citations', []),
            "trace_id": str(context.trace_id)
        }
        
        # Pass the generator if in streaming mode
        if context.streaming_mode and "generator" in result.metadata:
            metadata["generator"] = result.metadata["generator"]
            
        chat_response = ChatResponse(
            # Generate a consistent ID if no session conversation exists
            conversation_id="composed-conversation", 
            message=result.message if result else "No message.",
            metadata=metadata,
            used_tools=[t.get("tool") for t in getattr(result, 'tool_outputs', [])] if result else []
        )
        
        new_metadata = {**context.metadata, "chat_response": chat_response}
        return context.model_copy(update={"metadata": new_metadata})
