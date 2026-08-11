"""SQLite-backed conversation store.

Persists conversation metadata + full message history durably using the standard
library (blocking calls run on a worker thread so the event loop is never blocked).

Design notes
  - Every query is scoped by `user_id` (data isolation / auth hardening).
  - List/search return lightweight summaries (metadata columns only) so large
    histories are never parsed into memory until a single conversation is opened.
  - Pagination is pushed down to SQL (OFFSET/LIMIT) for efficient lazy loading.
"""
import asyncio
import datetime
import json
import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple

from app.conversations.models import (
    Conversation,
    ConversationMessage,
    ConversationType,
    MessageRole,
)


class SQLiteConversationStore:
    def __init__(self, db_path: str = "data/conversations.db"):
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
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id   TEXT PRIMARY KEY,
                    user_id           TEXT NOT NULL,
                    title             TEXT NOT NULL,
                    created_at        TEXT NOT NULL,
                    updated_at        TEXT NOT NULL,
                    last_message      TEXT NOT NULL DEFAULT '',
                    message_count     INTEGER NOT NULL DEFAULT 0,
                    favorite          INTEGER NOT NULL DEFAULT 0,
                    pinned            INTEGER NOT NULL DEFAULT 0,
                    archived          INTEGER NOT NULL DEFAULT 0,
                    conversation_type TEXT NOT NULL DEFAULT 'chat',
                    course_id         TEXT,
                    course_title      TEXT,
                    lesson_id         TEXT,
                    topic             TEXT,
                    progress          REAL,
                    assessment_id     TEXT,
                    assessment_score  TEXT,
                    tags              TEXT NOT NULL DEFAULT '[]',
                    messages_json     TEXT NOT NULL DEFAULT '[]'
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_conv_user_updated "
                "ON conversations (user_id, updated_at DESC)"
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_conv_user_fav "
                "ON conversations (user_id, favorite)"
            )
            self._conn.commit()
        return self._conn

    # ------------------------------------------------------------------ helpers
    def _row_to_conversation(self, row: sqlite3.Row, include_messages: bool) -> Conversation:
        messages = []
        if include_messages:
            for item in json.loads(row["messages_json"] or "[]"):
                messages.append(
                    ConversationMessage(
                        message_id=item.get("message_id", ""),
                        role=MessageRole(item["role"]),
                        content=item["content"],
                        created_at=datetime.datetime.fromisoformat(item["created_at"]),
                        metadata=item.get("metadata") or {},
                    )
                )
        return Conversation(
            conversation_id=row["conversation_id"],
            user_id=row["user_id"],
            title=row["title"],
            created_at=datetime.datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.datetime.fromisoformat(row["updated_at"]),
            last_message=row["last_message"],
            message_count=row["message_count"],
            favorite=bool(row["favorite"]),
            pinned=bool(row["pinned"]),
            archived=bool(row["archived"]),
            conversation_type=ConversationType(row["conversation_type"]),
            course_id=row["course_id"],
            course_title=row["course_title"],
            lesson_id=row["lesson_id"],
            topic=row["topic"],
            progress=row["progress"],
            assessment_id=row["assessment_id"],
            assessment_score=row["assessment_score"],
            tags=list(json.loads(row["tags"] or "[]")),
            messages=messages,
        )

    def _serialize_messages(self, conversation: Conversation) -> str:
        return json.dumps(
            [
                {
                    "message_id": m.message_id,
                    "role": m.role.value,
                    "content": m.content,
                    "created_at": m.created_at.isoformat(),
                    "metadata": m.metadata,
                }
                for m in conversation.messages
            ]
        )


    # ------------------------------------------------------------------ CRUD
    async def create(self, conversation: Conversation) -> Conversation:
        def _create():
            conn = self._connect()
            conn.execute(
                """INSERT INTO conversations (
                    conversation_id, user_id, title, created_at, updated_at,
                    last_message, message_count, favorite, pinned, archived,
                    conversation_type, course_id, course_title, lesson_id,
                    topic, progress, assessment_id, assessment_score, tags, messages_json
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                self._bind(conversation),
            )
            conn.commit()
        await asyncio.to_thread(_create)
        return conversation

    async def get(self, conversation_id: str, user_id: str) -> Optional[Conversation]:
        def _get():
            conn = self._connect()
            cur = conn.execute(
                "SELECT * FROM conversations WHERE conversation_id = ? AND user_id = ?",
                (conversation_id, user_id),
            )
            return cur.fetchone()
        row = await asyncio.to_thread(_get)
        return self._row_to_conversation(row, include_messages=True) if row else None

    async def update(self, conversation: Conversation) -> None:
        def _update():
            conn = self._connect()
            conn.execute(
                """UPDATE conversations SET
                    title=?, updated_at=?, last_message=?, message_count=?,
                    favorite=?, pinned=?, archived=?, conversation_type=?,
                    course_id=?, course_title=?, lesson_id=?, topic=?, progress=?,
                    assessment_id=?, assessment_score=?, tags=?, messages_json=?
                 WHERE conversation_id=? AND user_id=?""",
                (
                    conversation.title,
                    conversation.updated_at.isoformat(),
                    conversation.last_message,
                    conversation.message_count,
                    int(conversation.favorite),
                    int(conversation.pinned),
                    int(conversation.archived),
                    conversation.conversation_type.value,
                    conversation.course_id,
                    conversation.course_title,
                    conversation.lesson_id,
                    conversation.topic,
                    conversation.progress,
                    conversation.assessment_id,
                    conversation.assessment_score,
                    json.dumps(conversation.tags),
                    self._serialize_messages(conversation),
                    conversation.conversation_id,
                    conversation.user_id,
                ),
            )
            conn.commit()
        await asyncio.to_thread(_update)

    async def delete(self, conversation_id: str, user_id: str) -> bool:
        def _delete():
            conn = self._connect()
            cur = conn.execute(
                "DELETE FROM conversations WHERE conversation_id = ? AND user_id = ?",
                (conversation_id, user_id),
            )
            conn.commit()
            return cur.rowcount > 0
        return await asyncio.to_thread(_delete)

    # ------------------------------------------------------------------ list/search
    async def list(
        self,
        user_id: str,
        *,
        conversation_type: Optional[ConversationType] = None,
        favorite_only: Optional[bool] = None,
        include_archived: bool = False,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        days: Optional[int] = None,
    ) -> Tuple[List, int]:
        """Return (summaries, total). Most recently updated first.

        ``days`` restricts results to conversations updated within the last N
        days (Sprint 4: the sidebar shows the last 7 days; older chats are
        archived rather than shown).
        """
        where = ["user_id = ?"]
        params: List[object] = [user_id]

        if not include_archived:
            where.append("archived = 0")
        if conversation_type is not None:
            where.append("conversation_type = ?")
            params.append(conversation_type.value)
        if favorite_only is not None:
            where.append("favorite = ?")
            params.append(int(favorite_only))
        if days is not None and days > 0:
            cutoff = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).isoformat()
            where.append("updated_at >= ?")
            params.append(cutoff)
        if search:
            like = f"%{search}%"
            where.append(
                "(title LIKE ? OR last_message LIKE ? OR course_title LIKE ? "
                "OR course_id LIKE ? OR topic LIKE ? OR tags LIKE ? OR messages_json LIKE ?)"
            )
            params.extend([like] * 7)

        where_sql = " AND ".join(where)
        offset = max(0, (page - 1)) * page_size

        def _query():
            conn = self._connect()
            total = conn.execute(
                f"SELECT COUNT(*) AS c FROM conversations WHERE {where_sql}", params
            ).fetchone()["c"]
            rows = conn.execute(
                f"SELECT * FROM conversations WHERE {where_sql} "
                f"ORDER BY updated_at DESC LIMIT ? OFFSET ?",
                params + [page_size, offset],
            ).fetchall()
            return total, rows

        total, rows = await asyncio.to_thread(_query)
        summaries = [
            self._row_to_conversation(r, include_messages=False).summarize() for r in rows
        ]
        return summaries, total

    def _bind(self, conversation: Conversation) -> tuple:
        return (
            conversation.conversation_id,
            conversation.user_id,
            conversation.title,
            conversation.created_at.isoformat(),
            conversation.updated_at.isoformat(),
            conversation.last_message,
            conversation.message_count,
            int(conversation.favorite),
            int(conversation.pinned),
            int(conversation.archived),
            conversation.conversation_type.value,
            conversation.course_id,
            conversation.course_title,
            conversation.lesson_id,
            conversation.topic,
            conversation.progress,
            conversation.assessment_id,
            conversation.assessment_score,
            json.dumps(conversation.tags),
            self._serialize_messages(conversation),
        )

