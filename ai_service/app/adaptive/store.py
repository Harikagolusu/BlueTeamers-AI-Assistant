"""SQLite-backed persistence for the adaptive learning subsystem.

Stores learner profiles (base level + per-topic confidence), and
conversation-scoped session memory. Uses the standard library only; blocking
calls run on a worker thread so the event loop is never blocked.
"""
import asyncio
import datetime
import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional

from app.adaptive.models import (
    LearnerProfile,
    SessionMemoryState,
    TopicConfidence,
)
from app.adaptive.topics import TOPICS


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class SQLiteLearnerStore:
    def __init__(self, db_path: str = "data/adaptive.db"):
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
                CREATE TABLE IF NOT EXISTS learner_profiles (
                    user_id       TEXT PRIMARY KEY,
                    base_level    TEXT NOT NULL,
                    signal_counts TEXT NOT NULL,
                    updated_at    TEXT NOT NULL
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS topic_confidences (
                    user_id        TEXT NOT NULL,
                    topic_key      TEXT NOT NULL,
                    confidence     REAL NOT NULL,
                    evidence_count INTEGER NOT NULL,
                    last_seen      TEXT NOT NULL,
                    PRIMARY KEY (user_id, topic_key)
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS session_memory (
                    user_id          TEXT NOT NULL,
                    conversation_id  TEXT NOT NULL,
                    rolling_messages TEXT NOT NULL,
                    summary          TEXT NOT NULL DEFAULT '',
                    facts_json       TEXT NOT NULL DEFAULT '[]',
                    investigation    TEXT NOT NULL DEFAULT '{}',
                    files_json       TEXT NOT NULL DEFAULT '[]',
                    updated_at       TEXT NOT NULL,
                    PRIMARY KEY (user_id, conversation_id)
                )
                """
            )
            self._conn.commit()
        return self._conn

    # ------------------------------------------------------------------ profiles
    async def load_profile(self, user_id: str) -> LearnerProfile:
        def _load():
            conn = self._connect()
            row = conn.execute(
                "SELECT user_id, base_level, signal_counts, updated_at "
                "FROM learner_profiles WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            confs = conn.execute(
                "SELECT topic_key, confidence, evidence_count, last_seen "
                "FROM topic_confidences WHERE user_id = ?",
                (user_id,),
            ).fetchall()
            return row, confs

        row, conf_rows = await asyncio.to_thread(_load)
        if row is None:
            return LearnerProfile(user_id=user_id)

        profile = LearnerProfile(
            user_id=user_id,
            base_level=row["base_level"],
            signal_counts=json.loads(row["signal_counts"] or "{}"),
            updated_at=datetime.datetime.fromisoformat(row["updated_at"]),
        )
        for c in conf_rows:
            profile.topic_confidences[c["topic_key"]] = TopicConfidence(
                topic_key=c["topic_key"],
                confidence=c["confidence"],
                evidence_count=c["evidence_count"],
                last_seen=datetime.datetime.fromisoformat(c["last_seen"]),
            )
        return profile

    async def save_profile(self, profile: LearnerProfile) -> None:
        def _save():
            conn = self._connect()
            conn.execute(
                """
                INSERT INTO learner_profiles (user_id, base_level, signal_counts, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    base_level = excluded.base_level,
                    signal_counts = excluded.signal_counts,
                    updated_at = excluded.updated_at
                """,
                (
                    profile.user_id,
                    profile.base_level,
                    json.dumps(profile.signal_counts),
                    profile.updated_at.isoformat(),
                ),
            )
            for topic in TOPICS:
                conf = profile.topic_confidences.get(topic.key)
                if conf is None:
                    continue
                conn.execute(
                    """
                    INSERT INTO topic_confidences (user_id, topic_key, confidence, evidence_count, last_seen)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(user_id, topic_key) DO UPDATE SET
                        confidence = excluded.confidence,
                        evidence_count = excluded.evidence_count,
                        last_seen = excluded.last_seen
                    """,
                    (
                        profile.user_id,
                        conf.topic_key,
                        conf.confidence,
                        conf.evidence_count,
                        conf.last_seen.isoformat(),
                    ),
                )
            conn.commit()

        await asyncio.to_thread(_save)

    async def delete_profile(self, user_id: str) -> None:
        def _delete():
            conn = self._connect()
            conn.execute("DELETE FROM learner_profiles WHERE user_id = ?", (user_id,))
            conn.execute("DELETE FROM topic_confidences WHERE user_id = ?", (user_id,))
            conn.execute("DELETE FROM session_memory WHERE user_id = ?", (user_id,))
            conn.commit()

        await asyncio.to_thread(_delete)

    # ------------------------------------------------------------------ session memory
    async def load_session(self, user_id: str, conversation_id: Optional[str]) -> SessionMemoryState:
        if not conversation_id:
            return SessionMemoryState(user_id=user_id, conversation_id=None)

        def _load():
            conn = self._connect()
            row = conn.execute(
                "SELECT rolling_messages, summary, facts_json, investigation, files_json, updated_at "
                "FROM session_memory WHERE user_id = ? AND conversation_id = ?",
                (user_id, conversation_id),
            ).fetchone()
            return row

        row = await asyncio.to_thread(_load)
        if row is None:
            return SessionMemoryState(user_id=user_id, conversation_id=conversation_id)

        return SessionMemoryState(
            user_id=user_id,
            conversation_id=conversation_id,
            rolling_messages=json.loads(row["rolling_messages"] or "[]"),
            summary=row["summary"] or "",
            facts=json.loads(row["facts_json"] or "[]"),
            investigation=json.loads(row["investigation"] or "{}"),
            uploaded_files=json.loads(row["files_json"] or "[]"),
            updated_at=datetime.datetime.fromisoformat(row["updated_at"]),
        )

    async def save_session(self, state: SessionMemoryState) -> None:
        if not state.conversation_id:
            return

        def _save():
            conn = self._connect()
            conn.execute(
                """
                INSERT INTO session_memory (
                    user_id, conversation_id, rolling_messages, summary,
                    facts_json, investigation, files_json, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id, conversation_id) DO UPDATE SET
                    rolling_messages = excluded.rolling_messages,
                    summary = excluded.summary,
                    facts_json = excluded.facts_json,
                    investigation = excluded.investigation,
                    files_json = excluded.files_json,
                    updated_at = excluded.updated_at
                """,
                (
                    state.user_id,
                    state.conversation_id,
                    json.dumps(state.rolling_messages),
                    state.summary,
                    json.dumps(state.facts),
                    json.dumps(state.investigation),
                    json.dumps(state.uploaded_files),
                    state.updated_at.isoformat(),
                ),
            )
            conn.commit()

        await asyncio.to_thread(_save)

    async def delete_session(self, user_id: str, conversation_id: str) -> None:
        def _delete():
            conn = self._connect()
            conn.execute(
                "DELETE FROM session_memory WHERE user_id = ? AND conversation_id = ?",
                (user_id, conversation_id),
            )
            conn.commit()

        await asyncio.to_thread(_delete)
