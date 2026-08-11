from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.platform.context.user_context import UserContextBuilder

class PlatformContextLoadStage(IExecutionStage):
    """Retrieves the user's platform context (cached) and injects it into memory."""
    
    def __init__(self, user_context_builder: UserContextBuilder):
        self._user_context_builder = user_context_builder

    @property
    def name(self) -> str:
        return "LoadPlatformContext"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        token = context.metadata.get("token")
        if not token:
            return context
            
        platform_context_str = await self._user_context_builder.build(token)
        
        # Add to memory dictionary
        new_memory = dict(context.memory) if context.memory else {}
        new_memory["platform_context"] = platform_context_str
        
        return context.with_memory(new_memory)
