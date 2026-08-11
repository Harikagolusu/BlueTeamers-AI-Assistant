from typing import Dict, Any
from app.memory.interfaces import IMemoryManager
from app.memory.memory_service import MemoryService
from app.memory.models import MessageRole

class DefaultMemoryManager(IMemoryManager):
    """
    Adapter bridging the Chat Pipeline's IMemoryManager interface to the 
    underlying MemoryService which uses InMemoryStore.
    """
    def __init__(self, memory_service: MemoryService):
        self.memory_service = memory_service

    async def load_history(self, session_user: str, tenant_id: str) -> Dict[str, Any]:
        if not session_user:
            return {}
            
        messages = await self.memory_service.get_recent_messages(session_user)
        recent_text = ""
        for msg in messages:
            recent_text += f"{msg.role.value.capitalize()}: {msg.content}\n"
        
        return {
            "recent_context": recent_text.strip(),
            "messages": [{"role": m.role.value, "content": m.content} for m in messages]
        }

    async def save_turn(self, session_user: str, tenant_id: str, turn_data: Dict[str, Any]) -> None:
        if not session_user:
            return
            
        query = turn_data.get("query")
        response = turn_data.get("response")
        
        if query:
            await self.memory_service.append_message(session_user, MessageRole.USER, query)
        if response:
            await self.memory_service.append_message(session_user, MessageRole.ASSISTANT, response)
