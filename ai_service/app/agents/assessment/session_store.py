import threading
from typing import Dict, Optional

from app.agents.assessment.models import QuizSession


class InMemoryQuizSessionStore:
    """Thread-safe in-memory store of active quiz sessions, keyed by session_key.

    Kept behind a thin interface so it can later be swapped for a Redis/DB-backed
    store without touching the agent or pipeline.
    """

    def __init__(self):
        self._sessions: Dict[str, QuizSession] = {}
        self._lock = threading.RLock()

    def get(self, session_key: str) -> Optional[QuizSession]:
        with self._lock:
            session = self._sessions.get(session_key)
            return session.model_copy(deep=True) if session else None

    def put(self, session: QuizSession) -> None:
        with self._lock:
            self._sessions[session.session_key] = session.model_copy(deep=True)

    def delete(self, session_key: str) -> None:
        with self._lock:
            self._sessions.pop(session_key, None)

    def clear(self) -> None:
        with self._lock:
            self._sessions.clear()
