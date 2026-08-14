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
        """Atomically increment the user's usage counter and return the new count.

        The increment itself is atomic in SQLite, but the *limit check* must be
        part of the same statement to close the check-then-act race: concurrent
        requests that both read ``remaining > 0`` before either writes would
        otherwise all pass and push the counter past the configured limit.
        Callers use :meth:`increment_if_under` for limit-aware consumption.
        """
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

    async def increment_if_under(self, user_id: str, limit: int) -> Optional[int]:
        """Increment usage only if ``used < limit``; otherwise return None.

        The check and the increment execute as ONE SQL statement so concurrent
        requests can never overshoot the limit (no check-then-act window).
        Returns the new ``used`` count on success, or None when the daily
        allowance is exhausted.
        """
        def _try_incr():
            conn = self._connect()
            reset = self._current_reset()
            # Ensure a row exists for the window, then conditionally bump it.
            conn.execute(
                """
                INSERT OR IGNORE INTO daily_usage (user_id, reset_at, used)
                VALUES (?, ?, 0)
                """,
                (user_id, reset),
            )
            cur = conn.execute(
                """
                UPDATE daily_usage
                SET used = used + 1
                WHERE user_id = ? AND reset_at = ? AND used < ?
                """,
                (user_id, reset, limit),
            )
            conn.commit()
            if cur.rowcount == 0:
                return None
            row = conn.execute(
                "SELECT used FROM daily_usage WHERE user_id = ? AND reset_at = ?",
                (user_id, reset),
            ).fetchone()
            return int(row[_USED_KEY])

        return await asyncio.to_thread(_try_incr)

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

    async def carry_over(self, from_user_id: str, to_user_id: str) -> None:
        """Move usage accumulated under ``from_user_id`` (a guest key) onto
        ``to_user_id`` (the authenticated user), then drop the source row.

        The two identities represent the same person on the same device across a
        login boundary, so the count is shared rather than summed: the target
        keeps the larger of the two counts so the daily quota is never bypassed
        by logging in, and the stale guest row is pruned so the migration is
        idempotent on subsequent authenticated requests.
        """
        def _merge():
            conn = self._connect()
            reset = self._current_reset()
            src = conn.execute(
                "SELECT used FROM daily_usage WHERE user_id = ? AND reset_at = ?",
                (from_user_id, reset),
            ).fetchone()
            if src is None:
                return
            src_used = int(src[_USED_KEY])
            conn.execute(
                "DELETE FROM daily_usage WHERE user_id = ? AND reset_at = ?",
                (from_user_id, reset),
            )
            conn.execute(
                """
                INSERT INTO daily_usage (user_id, reset_at, used)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id, reset_at)
                DO UPDATE SET used = MAX(used, excluded.used)
                """,
                (to_user_id, reset, src_used),
            )
            conn.commit()

        await asyncio.to_thread(_merge)

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
