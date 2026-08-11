"""Freemium access models (Sprint 5).

A user is either:
  - PREMIUM — has purchased/enrolled in at least one course, unlimited usage.
  - FREE    — has no paid course, limited daily AI messages via the floating
              assistant. They may still browse history and read responses,
              only sending new messages is restricted.

The access-status payload is what the frontend needs to render the
"X / Y AI messages remaining today" indicator and the upgrade gate.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AccessLevel(str, Enum):
    PREMIUM = "premium"
    FREE = "free"


@dataclass(frozen=True)
class UsageState:
    """The usage counter for a user within the current reset window."""
    used: int
    limit: int
    reset: str  # ISO timestamp when the window resets


@dataclass(frozen=True)
class AccessStatus:
    """Full access summary returned by the /api/chat/access endpoint."""
    access_level: AccessLevel
    is_premium: bool
    enabled: bool  # False when the freemium feature flag is off
    limit: int
    used: int
    remaining: int
    reset_at: Optional[str] = None

    def can_send(self) -> bool:
        if not self.enabled:
            return True
        return self.access_level == AccessLevel.PREMIUM or self.remaining > 0

    def to_dict(self) -> dict:
        return {
            "access_level": self.access_level.value,
            "is_premium": self.is_premium,
            "enabled": self.enabled,
            "limit": self.limit,
            "used": self.used,
            "remaining": self.remaining,
            "reset_at": self.reset_at,
        }


@dataclass(frozen=True)
class AccessDecision:
    """Outcome of checking a chat request against the freemium limit."""
    allowed: bool
    status: AccessStatus
    reason: str = ""


class FreemiumLimitExceeded(Exception):
    """Raised when a free user has exhausted their message allowance."""

    def __init__(self, status: AccessStatus):
        super().__init__(
            "You've reached today's free AI limit. Purchase any BlueTeamers "
            "course to unlock unlimited AI assistance and the full AI Workspace."
        )
        self.status = status
