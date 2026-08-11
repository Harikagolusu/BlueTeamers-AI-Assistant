import logging
import time
from typing import List, Optional
from app.memory.interfaces import BaseMemoryStore
from app.memory.models import ConversationSession, MemoryMessage, MessageRole
from app.memory.exceptions import SessionNotFound
from app.observability.service import ObservabilityService

logger = logging.getLogger("app.memory.service")

class MemoryService:
    """
    Business logic layer for conversation memory.
    Enforces windowing logic and tracks sessions.
    """
    def __init__(
        self, 
        store: BaseMemoryStore, 
        enabled: bool = True,
        max_messages: int = 10,
        obs: Optional[ObservabilityService] = None
    ):
        self.store = store
        self.enabled = enabled
        self.max_messages = max_messages
        self.obs = obs

    async def session_exists(self, session_id: str) -> bool:
        if not self.enabled:
            return False
        session = await self.store.get_session(session_id)
        return session is not None

    async def create_session(self, session_id: str) -> ConversationSession:
        if not self.enabled:
            return ConversationSession(session_id=session_id)
        session = await self.store.create_session(session_id)
        logger.info(f"Created new conversation session - SessionID: {session_id}")
        if self.obs:
            self.obs.increment_gauge("conversation_active_total", 1.0, {"memory_backend": "in_memory"})
        return session

    async def get_recent_messages(self, session_id: str) -> List[MemoryMessage]:
        if not self.enabled:
            return []
            
        start_time = time.time()
        session = await self.store.get_session(session_id)
        if not session:
            # Auto-create if it doesn't exist to remain frictionless
            session = await self.create_session(session_id)
            
        if self.obs:
            self.obs.observe_histogram("memory_lookup_latency_seconds", time.time() - start_time, {"memory_backend": "in_memory"})
            self.obs.increment_counter("conversation_memory_reads_total", 1.0)
            
        return session.messages

    async def append_message(self, session_id: str, role: MessageRole, content: str) -> None:
        if not self.enabled:
            return
            
        session = await self.store.get_session(session_id)
        if not session:
            session = await self.create_session(session_id)
            
        msg = MemoryMessage(role=role, content=content)
        session.messages.append(msg)
        
        # Enforce memory window
        if len(session.messages) > self.max_messages:
            session.messages = session.messages[-self.max_messages:]
            
        await self.store.update_session(session)
        logger.info(f"Appended message to session - SessionID: {session_id} - Role: {role.value}")
        
        if self.obs:
            self.obs.increment_counter("conversation_memory_writes_total", 1.0)

    async def clear_conversation(self, session_id: str) -> None:
        if not self.enabled:
            return
            
        session = await self.store.get_session(session_id)
        if not session:
            raise SessionNotFound(f"Session {session_id} not found")
            
        session.messages = []
        await self.store.update_session(session)
        logger.info(f"Cleared conversation - SessionID: {session_id}")

    async def delete_session(self, session_id: str) -> bool:
        if not self.enabled:
            return False
            
        success = await self.store.delete_session(session_id)
        if success:
            logger.info(f"Deleted conversation session - SessionID: {session_id}")
            if self.obs:
                self.obs.decrement_gauge("conversation_active_total", 1.0, {"memory_backend": "in_memory"})
        return success
