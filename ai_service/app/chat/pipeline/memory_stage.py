from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.memory.interfaces import IMemoryManager

class MemoryLoadStage(IExecutionStage):
    """Retrieves conversation history and injects it into the context."""
    
    def __init__(self, memory_manager: IMemoryManager):
        self._memory = memory_manager

    @property
    def name(self) -> str:
        return "LoadMemory"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if not context.session_user:
            # Cannot load memory for anonymous users, return context as-is
            return context

        history = await self._memory.load_history(
            session_user=_memory_session_user(context),
            tenant_id=context.tenant_id or "default"
        )

        # Returns a new context object due to immutability
        return context.with_memory(history)


def _memory_session_user(context: ExecutionContext) -> str:
    """Scope the short-term memory window per conversation.

    Without a conversation id the memory falls back to the per-user window so
    anonymous / pre-conversation requests behave exactly as before. When a
    conversation exists, memory is isolated to that conversation (Sprint 4:
    context isolation), preventing topics from bleeding across chats.
    """
    conversation_id = context.metadata.get("conversation_id")
    if conversation_id:
        return f"{context.session_user}::{conversation_id}"
    return context.session_user
