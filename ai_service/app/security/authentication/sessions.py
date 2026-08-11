import uuid
from typing import Dict
from app.security.interfaces.i_authentication import ISessionManager

class InMemorySessionManager(ISessionManager):
    def __init__(self):
        self._sessions: Dict[str, str] = {} # session_id -> principal

    def create_session(self, principal: str) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = principal
        return session_id

    def validate_session(self, session_id: str) -> bool:
        return session_id in self._sessions

    def invalidate_session(self, session_id: str) -> None:
        if session_id in self._sessions:
            del self._sessions[session_id]
