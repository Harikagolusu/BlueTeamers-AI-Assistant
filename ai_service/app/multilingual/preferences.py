"""Per-user language preference persistence (Feature 6 — conversation memory).

Stores the user's *preferred language mode* (a concrete language code or
``auto``) in a dedicated SQLite database. Keeping a separate DB instead of
touching the Django user profile means the feature is fully self-contained and
adds no schema changes to the existing platform, while still persisting across
conversations and sessions for a given user.

Blocking calls run on a worker thread via ``asyncio.to_thread`` so the event
loop is never blocked (same pattern as the adaptive-learner store).
"""
import asyncio
import datetime
import sqlite3
from pathlib import Path
from typing import Optional

from app.multilingual.languages import is_supported_code


def _utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class LanguagePreferenceStore:
    """SQLite-backed storage for a user's chosen language mode."""

    def __init__(self, db_path: str = "data/language_prefs.db"):
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
                CREATE TABLE IF NOT EXISTS language_preferences (
                    user_id    TEXT PRIMARY KEY,
                    language   TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            self._conn.commit()
        return self._conn

    async def get(self, user_id: str) -> Optional[str]:
        """Return the stored language mode for the user, or None."""
        def _get() -> Optional[str]:
            row = self._connect().execute(
                "SELECT language FROM language_preferences WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            return row["language"] if row else None
        return await asyncio.to_thread(_get)

    async def set(self, user_id: str, language: str) -> None:
        """Persist the user's language mode (upsert)."""
        if not is_supported_code(language):
            raise ValueError(f"Unsupported language code: {language!r}")

        def _set() -> None:
            conn = self._connect()
            conn.execute(
                """
                INSERT INTO language_preferences (user_id, language, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    language = excluded.language,
                    updated_at = excluded.updated_at
                """,
                (user_id, language, _utc_now()),
            )
            conn.commit()
        await asyncio.to_thread(_set)

    async def clear(self, user_id: str) -> None:
        """Remove the stored preference (user switched back to Auto Detect)."""

        def _clear() -> None:
            conn = self._connect()
            conn.execute("DELETE FROM language_preferences WHERE user_id = ?", (user_id,))
            conn.commit()
        await asyncio.to_thread(_clear)