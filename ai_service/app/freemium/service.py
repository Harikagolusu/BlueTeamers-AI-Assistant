"""Freemium access service (Sprint 5).

Determines a user's access level (premium vs free) from their Django course
purchases and enforces the daily message limit for free users.

Premium check is cached in-process for a short TTL so the chat hot path does
not hit Django on every request, while a fresh purchase is still honoured
within a minute.
"""
import asyncio
import logging
import time
from typing import Dict, Optional, Tuple

from app.core.config import settings
from app.freemium.models import (
    AccessDecision,
    AccessLevel,
    AccessStatus,
    FreemiumLimitExceeded,
    UsageState,
)
from app.freemium.store import FreemiumStore
from app.platform.repositories.interfaces import IPlatformRepository

logger = logging.getLogger("app.freemium.service")

_PREMIUM_CACHE_TTL_SECONDS = 60


class FreemiumService:
    """Application service enforcing the free/premium AI access rules."""

    def __init__(
        self,
        store: FreemiumStore,
        platform_repo: Optional[IPlatformRepository] = None,
    ):
        self._store = store
        self._platform_repo = platform_repo
        self._premium_cache: Dict[str, Tuple[bool, float]] = {}

    # ------------------------------------------------------------------ config
    def _enabled(self) -> bool:
        return bool(getattr(settings, "FREEMIUM_ENABLED", True))

    def _free_limit(self) -> int:
        limit = int(getattr(settings, "FREEMIUM_FREE_MESSAGE_LIMIT", 5))
        return max(1, limit)

    def _premium_statuses(self) -> set:
        raw = getattr(settings, "FREEMIUM_PREMIUM_PURCHASE_STATUSES", "paid")
        return {s.strip().lower() for s in raw.split(",") if s.strip()}

    # ------------------------------------------------------------------ access
    async def is_premium(self, user_id: str, token: str) -> bool:
        """Whether the user holds at least one paid course purchase."""
        if not self._platform_repo or not token:
            return False
        now = time.time()
        cached = self._premium_cache.get(user_id)
        if cached and (now - cached[1]) < _PREMIUM_CACHE_TTL_SECONDS:
            return cached[0]
        try:
            purchases = await self._platform_repo.get_purchases(token)
            paid_statuses = self._premium_statuses()
            premium = any(
                (p.status or "").lower() in paid_statuses for p in purchases
            )
        except Exception as e:  # Django down / auth failure -> treat as free
            logger.warning(f"Failed to resolve premium status for {user_id}: {e}")
            premium = False
        self._premium_cache[user_id] = (premium, now)
        return premium

    async def get_access_status(self, user_id: str, token: str) -> AccessStatus:
        """Full access summary for the current user."""
        enabled = self._enabled()
        if not enabled:
            return AccessStatus(
                access_level=AccessLevel.PREMIUM,
                is_premium=True,
                enabled=False,
                limit=0,
                used=0,
                remaining=0,
                reset_at=None,
            )
        if user_id and await self.is_premium(user_id, token):
            return AccessStatus(
                access_level=AccessLevel.PREMIUM,
                is_premium=True,
                enabled=True,
                limit=0,
                used=0,
                remaining=0,
                reset_at=None,
            )
        limit = self._free_limit()
        if not user_id:
            return AccessStatus(
                access_level=AccessLevel.FREE,
                is_premium=False,
                enabled=True,
                limit=limit,
                used=0,
                remaining=limit,
                reset_at=None,
            )
        usage: UsageState = await self._store.load(user_id)
        return AccessStatus(
            access_level=AccessLevel.FREE,
            is_premium=False,
            enabled=True,
            limit=limit,
            used=usage.used,
            remaining=max(0, limit - usage.used),
            reset_at=usage.reset,
        )

    async def check_and_consume(self, user_id: str, token: str) -> AccessDecision:
        """Validate and (for free users) consume one message slot.

        Raises FreemiumLimitExceeded when a free user is out of messages.
        """
        status = await self.get_access_status(user_id, token)
        if not status.enabled or status.is_premium:
            return AccessDecision(allowed=True, status=status)
        if status.remaining <= 0:
            raise FreemiumLimitExceeded(status)
        if not user_id:
            return AccessDecision(allowed=True, status=status)
        used = await self._store.increment(user_id)
        status = AccessStatus(
            access_level=status.access_level,
            is_premium=status.is_premium,
            enabled=status.enabled,
            limit=status.limit,
            used=used,
            remaining=max(0, status.limit - used),
            reset_at=status.reset_at,
        )
        return AccessDecision(allowed=True, status=status)

    async def invalidate(self, user_id: str) -> None:
        """Drop cached premium status (e.g. after a purchase confirmation)."""
        self._premium_cache.pop(user_id, None)
        if self._store:
            try:
                await self._store.reset(user_id)
            except Exception as e:
                logger.warning(f"Failed to reset freemium usage for {user_id}: {e}")
