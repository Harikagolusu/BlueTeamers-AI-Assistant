from typing import Dict, Optional
import asyncio
import datetime
import json
import sqlite3
from pathlib import Path

from app.memory.interfaces import BaseMemoryStore
from app.memory.models import ConversationSession, MemoryMessage, MessageRole

class InMemoryStore(BaseMemoryStore):
    """
    In-memory dictionary backed storage implementation.
    Production-ready for single-instance, but should be replaced by
    RedisStore in a distributed environment.
    """
    def __init__(self):
        self._store: Dict[str, ConversationSession] = {}
        self._lock = asyncio.Lock()

    async def create_session(self, session_id: str) -> ConversationSession:
        async with self._lock:
            session = ConversationSession(session_id=session_id)
            self._store[session_id] = session
            return session

    async def get_session(self, session_id: str) -> Optional[ConversationSession]:
        async with self._lock:
            # Return a copy to avoid mutation outside of update
            session = self._store.get(session_id)
            if session:
                return session.model_copy(deep=True)
            return None

    async def update_session(self, session: ConversationSession) -> None:
        async with self._lock:
            self._store[session.session_id] = session.model_copy(deep=True)

    async def delete_session(self, session_id: str) -> bool:
        async with self._lock:
            if session_id in self._store:
                del self._store[session_id]
                return True
            return False

    async def health_check(self) -> dict:
        async with self._lock:
            return {
                "status": "healthy",
                "backend": "in_memory",
                "active_sessions": len(self._store)
            }


class SQLiteStore(BaseMemoryStore):
    """
    SQLite-backed conversation memory store.

    Provides real persistence across process restarts using only the standard
    library (sqlite3). Blocking calls are dispatched to a worker thread so the
    event loop is never blocked. Suitable for single-instance deployments; swap
    for a Postgres/Redis store when scaling horizontally.
    """
    def __init__(self, db_path: str = "data/memory.db"):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def _connect(self) -> sqlite3.Connection:
        if self._conn is None:
            path = Path(self.db_path)
            if path.parent and not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(path), check_same_thread=False, timeout=30)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation_sessions (
                    session_id   TEXT PRIMARY KEY,
                    created_at   TEXT NOT NULL,
                    messages_json TEXT NOT NULL
                )
                """
            )
            self._conn.commit()
        return self._conn

    def _serialize_messages(self, session: ConversationSession) -> str:
        return json.dumps(
            [
                {
                    "role": m.role.value,
                    "content": m.content,
                    "timestamp": m.timestamp.isoformat(),
                }
                for m in session.messages
            ]
        )

    def _deserialize_messages(self, row: sqlite3.Row) -> ConversationSession:
        messages = []
        for item in json.loads(row["messages_json"]):
            messages.append(
                MemoryMessage(
                    role=MessageRole(item["role"]),
                    content=item["content"],
                    timestamp=datetime.datetime.fromisoformat(item["timestamp"]),
                )
            )
        return ConversationSession(
            session_id=row["session_id"],
            created_at=datetime.datetime.fromisoformat(row["created_at"]),
            messages=messages,
        )

    async def create_session(self, session_id: str) -> ConversationSession:
        def _create():
            conn = self._connect()
            now = datetime.datetime.now(datetime.timezone.utc)
            conn.execute(
                "INSERT OR IGNORE INTO conversation_sessions (session_id, created_at, messages_json) VALUES (?, ?, ?)",
                (session_id, now.isoformat(), "[]"),
            )
            conn.commit()
        await asyncio.to_thread(_create)
        session = await self.get_session(session_id)
        return session or ConversationSession(session_id=session_id)

    async def get_session(self, session_id: str) -> Optional[ConversationSession]:
        def _get():
            conn = self._connect()
            cur = conn.execute(
                "SELECT session_id, created_at, messages_json FROM conversation_sessions WHERE session_id = ?",
                (session_id,),
            )
            return cur.fetchone()
        row = await asyncio.to_thread(_get)
        if row is None:
            return None
        return self._deserialize_messages(row)

    async def update_session(self, session: ConversationSession) -> None:
        def _update():
            conn = self._connect()
            conn.execute(
                """
                INSERT INTO conversation_sessions (session_id, created_at, messages_json)
                VALUES (?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET messages_json = excluded.messages_json
                """,
                (session.session_id, session.created_at.isoformat(), self._serialize_messages(session)),
            )
            conn.commit()
        await asyncio.to_thread(_update)

    async def delete_session(self, session_id: str) -> bool:
        def _delete():
            conn = self._connect()
            cur = conn.execute(
                "DELETE FROM conversation_sessions WHERE session_id = ?",
                (session_id,),
            )
            conn.commit()
            return cur.rowcount > 0
        return await asyncio.to_thread(_delete)

    async def health_check(self) -> dict:
        def _health():
            try:
                conn = self._connect()
                count = conn.execute("SELECT COUNT(*) AS c FROM conversation_sessions").fetchone()["c"]
                return {
                    "status": "healthy",
                    "backend": "sqlite",
                    "active_sessions": count,
                    "db_path": self.db_path,
                }
            except Exception as e:  # pragma: no cover
                return {"status": "unhealthy", "backend": "sqlite", "error": str(e)}
        return await asyncio.to_thread(_health)
