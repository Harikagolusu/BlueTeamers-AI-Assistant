"""AdaptiveLearningService: facade over the learner engine + session memory."""
from typing import Dict, List, Optional, Sequence

from app.adaptive.engine import AdaptiveLearningEngine
from app.adaptive.models import (
    LearnerAdaptation,
    SessionMemoryState,
)
from app.adaptive.session_memory import SessionMemoryManager
from app.adaptive.store import SQLiteLearnerStore


class AdaptiveLearningService:
    def __init__(
        self,
        engine: AdaptiveLearningEngine,
        session_memory: SessionMemoryManager,
        store: SQLiteLearnerStore,
    ):
        self.engine = engine
        self.session_memory = session_memory
        self.store = store

    async def adapt(
        self,
        user_id: str,
        query: str,
        recent_texts: Sequence[str] = (),
    ) -> LearnerAdaptation:
        """Compute the per-request teaching plan (no persistence)."""
        return await self.engine.adapt(user_id, query, recent_texts)

    async def load_session(self, user_id: str, conversation_id: Optional[str]) -> SessionMemoryState:
        return await self.session_memory.load(user_id, conversation_id)

    async def observe_turn(
        self,
        user_id: str,
        conversation_id: Optional[str],
        query: str,
        ai_message: str,
        adaptation: LearnerAdaptation,
        engine: Optional[str] = None,
        files: Optional[List[dict]] = None,
        images: Optional[List[str]] = None,
    ) -> Dict:
        """Persist the learner-model update + session memory for one turn."""
        await self.engine.observe(
            user_id,
            adaptation.topic_keys,
            adaptation.signals,
        )
        session = await self.session_memory.record_turn(
            user_id,
            conversation_id,
            query,
            ai_message,
            topic_keys=adaptation.topic_keys,
            engine=engine,
            files=files,
            images=images,
        )
        return {"profile_updated": True, "session": session.to_dict()}
