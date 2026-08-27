"""Persistent, dual-window (daily + monthly) token quota manager.

Implements the existing :class:`IQuotaManager` interface used by the runtime
governance layer. It is intentionally **audit-first**: usage is always recorded
to SQLite so the team can measure real consumption; blocking is opt-in via an
``enforce`` flag (``TOKEN_QUOTA_ENFORCE``), which you flip on once you've picked
realistic daily/monthly limits from the measured data.
"""

import logging
import datetime

from typing import Optional

from app.runtime.interfaces.governance import IQuotaManager
from app.runtime.services.token_usage_store import TokenUsageStore

logger = logging.getLogger("app.runtime.token_quota")


class PersistentTokenQuotaManager(IQuotaManager):
    """Enforces (optionally) and always records per-user token usage."""

    def __init__(
        self,
        store: TokenUsageStore,
        daily_limit: int = 100_000,
        monthly_limit: int = 2_000_000,
        enforce: bool = False,
    ):
        self._store = store
        self.daily_limit = int(daily_limit)
        self.monthly_limit = int(monthly_limit)
        self.enforce = bool(enforce)

    # ------------------------------------------------ IQuotaManager
    async def check_quota(self, user_id: str) -> bool:
        """Whether a request from ``user_id`` may proceed.

        In audit mode this always returns True (we record, we don't block).
        When enforcement is on, the request is denied if the user has already
        consumed at least their daily OR monthly limit.
        """
        if not self.enforce:
            return True
        daily = await self._store.get_used(user_id, "daily")
        if daily >= self.daily_limit:
            logger.info(
                "Token quota exceeded (daily) for %s: used %d >= limit %d",
                user_id, daily, self.daily_limit,
            )
            return False
        monthly = await self._store.get_used(user_id, "monthly")
        if monthly >= self.monthly_limit:
            logger.info(
                "Token quota exceeded (monthly) for %s: used %d >= limit %d",
                user_id, monthly, self.monthly_limit,
            )
            return False
        return True

    async def increment_usage(self, user_id: str, tokens: int, display_name: str = None, email: str = None) -> None:
        """Record ``tokens`` consumed by ``user_id`` in both windows.

        Always runs (even in audit mode) so measured usage is persisted.
        When a human-readable ``display_name``/``email`` is supplied (authenticated
        users), it is persisted alongside the scope so ``overview`` can show who
        is who instead of just ``user:1``.
        """
        if not user_id or tokens <= 0:
            return
        # Persist name mapping best-effort before counting tokens.
        if display_name or email:
            try:
                await self._store.set_display_name(user_id, display_name, email)
            except Exception:
                pass
        await self._store.add_tokens(user_id, "daily", tokens)
        await self._store.add_tokens(user_id, "monthly", tokens)

    # ---------------------------------------------- convenience
    async def get_status(self, user_id: str) -> dict:
        """Snapshot of a user's daily + monthly usage for reporting/UX."""
        daily = await self._store.get_used(user_id, "daily")
        monthly = await self._store.get_used(user_id, "monthly")
        meta = await self._store.get_display_name(user_id) if hasattr(self._store, "get_display_name") else None
        return {
            "scope": user_id,
            "display_name": (meta or {}).get("display_name") if meta else None,
            "email": (meta or {}).get("email") if meta else None,
            "daily_used": daily,
            "daily_limit": self.daily_limit,
            "daily_remaining": max(0, self.daily_limit - daily),
            "monthly_used": monthly,
            "monthly_limit": self.monthly_limit,
            "monthly_remaining": max(0, self.monthly_limit - monthly),
            "enforce": self.enforce,
        }

    async def overview(self) -> dict:
        """Live consumption across every scope (for the team monitor).

        Aggregates today's and this month's usage per user/device and sorts by
        daily consumption (highest first) so heavy consumers are visible at a
        glance.
        """
        snapshot = await self._store.snapshot()
        for entry in snapshot:
            entry["daily_limit"] = self.daily_limit
            entry["daily_remaining"] = max(0, self.daily_limit - entry["daily_used"])
            entry["daily_pct"] = round(entry["daily_used"] * 100.0 / self.daily_limit, 1) if self.daily_limit else 0.0
            entry["monthly_limit"] = self.monthly_limit
            entry["monthly_remaining"] = max(0, self.monthly_limit - entry["monthly_used"])
            entry["monthly_pct"] = round(entry["monthly_used"] * 100.0 / self.monthly_limit, 1) if self.monthly_limit else 0.0
        snapshot.sort(key=lambda e: e["daily_used"], reverse=True)
        return {
            "daily_limit": self.daily_limit,
            "monthly_limit": self.monthly_limit,
            "enforce": self.enforce,
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "users": snapshot,
        }