"""SQLite-backed persistence for the freemium usage tracking (Sprint 5).

A single ``daily_usage`` table records how many AI requests each user has made
within the current reset window. Blocking calls run on a worker thread so the
event loop is never blocked (matches the adaptive-learning store pattern).
"""
import asyncio
import datetime
import sqlite3
from pathlib import Path
from typing import Optional

from app.freemium.models import UsageState

_RESET_KEY = "reset_at"
_USED_KEY = "used"


def _utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _day_start(dt: datetime.datetime) -> datetime.datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


class FreemiumStore:
    """Tracks per-user AI usage in SQLite. Safe to share across requests."""

    def __init__(self, db_path: str = "data/freemium.db"):
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
                CREATE TABLE IF NOT EXISTS daily_usage (
                    user_id    TEXT NOT NULL,
                    reset_at   TEXT NOT NULL,
                    used       INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY (user_id, reset_at)
                )
                """
            )
            self._conn.commit()
        return self._conn

    async def load(self, user_id: str) -> UsageState:
        """Return the user's usage for the current window (0 when fresh)."""
        def _load():
            conn = self._connect()
            row = conn.execute(
                "SELECT reset_at, used FROM daily_usage "
                "WHERE user_id = ? AND reset_at = ?",
                (user_id, self._current_reset()),
            ).fetchone()
            if row is None:
                return UsageState(used=0, limit=0, reset=self._current_reset())
            return UsageState(
                used=int(row[_USED_KEY]),
                limit=0,
                reset=str(row[_RESET_KEY]),
            )

        return await asyncio.to_thread(_load)

    async def increment(self, user_id: str) -> int:
        """Increment the user's usage counter and return the new count."""
        def _incr():
            conn = self._connect()
            reset = self._current_reset()
            conn.execute(
                """
                INSERT INTO daily_usage (user_id, reset_at, used)
                VALUES (?, ?, 1)
                ON CONFLICT(user_id, reset_at)
                DO UPDATE SET used = used + 1
                """,
                (user_id, reset),
            )
            conn.commit()
            row = conn.execute(
                "SELECT used FROM daily_usage WHERE user_id = ? AND reset_at = ?",
                (user_id, reset),
            ).fetchone()
            return int(row[_USED_KEY])

        return await asyncio.to_thread(_incr)

    async def reset(self, user_id: str) -> None:
        """Clear the user's usage in the current window (used on upgrade)."""
        def _reset():
            conn = self._connect()
            conn.execute(
                "DELETE FROM daily_usage WHERE user_id = ?",
                (user_id,),
            )
            conn.commit()

        await asyncio.to_thread(_reset)

    def _current_reset(self) -> str:
        """Compute the reset-window key from the configured policy.

        Only ``daily`` is supported as a dedicated window today; any other
        value (e.g. "never") returns a fixed epoch key so the counter never
        resets automatically. This keeps the reset policy configurable without
        special-casing the SQL in the calling code.
        """
        from app.core.config import settings

        policy = (settings.FREEMIUM_RESET_POLICY or "daily").lower()
        now = _utc_now()
        if policy == "daily":
            return _day_start(now).isoformat()
        return "epoch"
