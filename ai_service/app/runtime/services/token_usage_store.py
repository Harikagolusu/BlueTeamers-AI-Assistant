"""SQLite-backed persistence for the per-user token usage counter.

A single ``token_usage`` table records how many LLM tokens each identity has
consumed. Scopes follow the runtime governance convention: an authenticated
user is keyed as ``user:<id>`` and an anonymous caller as ``ip:<address>``
(the transport peer IP, not the spoofable client id) so colleagues testing over
the same network share one bucket — which is exactly what we want while
measuring baseline usage.

Each row is keyed by ``(scope, period)``, where ``period`` pins the row to a
UTC day (``daily|2026-08-26``) or a calendar month (``monthly|2026-08``), so the
daily and monthly totals roll over independently each window. Blocking DB calls
run on a worker thread so the event loop is never blocked (matches the freemium
store pattern).
"""

import asyncio
import datetime
import sqlite3
import threading
from pathlib import Path
from typing import Optional

_DAY_FORMAT = "%Y-%m-%d"
_MONTH_FORMAT = "%Y-%m"


def _utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _day_key(dt: datetime.datetime) -> str:
    return dt.strftime(_DAY_FORMAT)


def _month_key(dt: datetime.datetime) -> str:
    return dt.strftime(_MONTH_FORMAT)


class TokenUsageStore:
    """Per-user token accounting backed by SQLite. Safe to share across requests."""

    def __init__(self, db_path: str = "data/token_quota.db"):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        # Guards the read-modify-write of a single bucket so concurrent
        # requests cannot race on the same counter.
        self._lock = threading.Lock()

    def _connect(self) -> sqlite3.Connection:
        if self._conn is None:
            path = Path(self.db_path)
            if path.parent and not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(path), check_same_thread=False, timeout=30)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS token_usage (
                    scope   TEXT NOT NULL,
                    period  TEXT NOT NULL,
                    used    INTEGER NOT NULL DEFAULT 0,
                    PRIMARY KEY (scope, period)
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS token_user_meta (
                    scope        TEXT PRIMARY KEY,
                    display_name TEXT,
                    email        TEXT,
                    updated_at   TEXT
                )
                """
            )
            self._conn.commit()
        return self._conn

    async def set_display_name(self, scope: str, display_name: Optional[str], email: Optional[str] = None) -> None:
        """Persist human-readable name for a scope (best-effort, never fails)."""
        if not scope or not (display_name or email):
            return

        def _set():
            conn = self._connect()
            with self._lock:
                conn.execute(
                    """
                    INSERT INTO token_user_meta (scope, display_name, email, updated_at)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(scope) DO UPDATE SET
                        display_name = COALESCE(excluded.display_name, display_name),
                        email = COALESCE(excluded.email, email),
                        updated_at = excluded.updated_at
                    """,
                    (scope, display_name, email, _utc_now().isoformat()),
                )
                conn.commit()

        await asyncio.to_thread(_set)

    async def get_display_name(self, scope: str) -> Optional[dict]:
        def _get():
            row = self._connect().execute(
                "SELECT display_name, email FROM token_user_meta WHERE scope = ?",
                (scope,),
            ).fetchone()
            if row:
                return {"display_name": row["display_name"], "email": row["email"]}
            return None

        return await asyncio.to_thread(_get)

    def _period(self, window: str) -> str:
        now = _utc_now()
        if window == "daily":
            return f"daily|{_day_key(now)}"
        if window == "monthly":
            return f"monthly|{_month_key(now)}"
        raise ValueError(f"Unknown window: {window}")

    async def get_used(self, scope: str, window: str) -> int:
        """Return tokens consumed by ``scope`` in the given window."""

        def _get():
            period = self._period(window)
            row = self._connect().execute(
                "SELECT used FROM token_usage WHERE scope = ? AND period = ?",
                (scope, period),
            ).fetchone()
            return int(row["used"]) if row else 0

        return await asyncio.to_thread(_get)

    async def snapshot(self) -> list:
        """Return today's and this month's usage for every recorded scope.

        Used by the live consumption monitor: each item is a dict with
        ``scope``, ``daily_used`` and ``monthly_used`` (0 when the scope has no
        row yet for that window).
        """
        daily_period = self._period("daily")
        monthly_period = self._period("monthly")

        def _snap():
            rows = self._connect().execute(
                "SELECT scope, period, used FROM token_usage "
                "WHERE period IN (?, ?)",
                (daily_period, monthly_period),
            ).fetchall()
            # Also pull stored display names in one pass.
            meta_rows = self._connect().execute(
                "SELECT scope, display_name, email FROM token_user_meta"
            ).fetchall()
            meta_map = {r["scope"]: {"display_name": r["display_name"], "email": r["email"]} for r in meta_rows}
            buckets: dict = {}
            for r in rows:
                scope = r["scope"]
                entry = buckets.setdefault(
                    scope, {"scope": scope, "daily_used": 0, "monthly_used": 0}
                )
                if r["period"] == daily_period:
                    entry["daily_used"] = int(r["used"])
                else:
                    entry["monthly_used"] = int(r["used"])
            # Enrich with display_name/email (keeps existing scope for backward compat).
            for scope, entry in buckets.items():
                meta = meta_map.get(scope) or {}
                entry["display_name"] = meta.get("display_name")
                entry["email"] = meta.get("email")
            return list(buckets.values())

        return await asyncio.to_thread(_snap)

    async def add_tokens(self, scope: str, window: str, tokens: int) -> int:
        """Unconditionally add ``tokens`` to a window and return the new total.

        This is the accounting path for audit mode and for billing a completed
        request. It never blocks — enforcement, when enabled, is a separate,
        opt-in check done against the same table.
        """
        period = self._period(window)
        tokens = max(0, int(tokens))

        def _add():
            conn = self._connect()
            with self._lock:
                conn.execute(
                    """
                    INSERT INTO token_usage (scope, period, used)
                    VALUES (?, ?, ?)
                    ON CONFLICT(scope, period)
                    DO UPDATE SET used = used + excluded.used
                    """,
                    (scope, period, tokens),
                )
                conn.commit()
                row = conn.execute(
                    "SELECT used FROM token_usage WHERE scope = ? AND period = ?",
                    (scope, period),
                ).fetchone()
                return int(row["used"])

        return await asyncio.to_thread(_add)

    async def consume_if_under(self, scope: str, window: str, tokens: int, limit: int) -> Optional[int]:
        """Atomically add ``tokens`` to a window only if it stays within ``limit``.

        Returns the new total on success, or ``None`` when accepting the tokens
        would exceed the limit. The check and the update happen inside one SQL
        statement, closing the check-then-act race. Used only when enforcement
        is enabled.
        """
        period = self._period(window)
        tokens = max(0, int(tokens))

        def _try():
            conn = self._connect()
            with self._lock:
                conn.execute(
                    "INSERT OR IGNORE INTO token_usage (scope, period, used) VALUES (?, ?, 0)",
                    (scope, period),
                )
                cur = conn.execute(
                    """
                    UPDATE token_usage
                    SET used = used + ?
                    WHERE scope = ? AND period = ? AND used + ? <= ?
                    """,
                    (tokens, scope, period, tokens, limit),
                )
                conn.commit()
                if cur.rowcount == 0:
                    return None
                row = conn.execute(
                    "SELECT used FROM token_usage WHERE scope = ? AND period = ?",
                    (scope, period),
                ).fetchone()
                return int(row["used"])

        return await asyncio.to_thread(_try)

    async def reset(self, scope: str) -> None:
        """Clear all recorded usage for a scope (used on manual override)."""

        def _reset():
            conn = self._connect()
            conn.execute("DELETE FROM token_usage WHERE scope = ?", (scope,))
            conn.commit()

        await asyncio.to_thread(_reset)

    def prune_old(self) -> int:
        """Drop rows for stale windows so the table stays bounded (rollover
        buckets older than the current UTC day/month are expendable history).
        Called opportunistically on startup."""
        now = _utc_now()
        keep = (f"daily|{_day_key(now)}", f"monthly|{_month_key(now)}")
        try:
            conn = self._connect()
            cur = conn.execute(
                "DELETE FROM token_usage WHERE period NOT IN (?, ?)",
                (keep[0], keep[1]),
            )
            conn.commit()
            return cur.rowcount
        except Exception:
            return 0