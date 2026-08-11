"""Freemium AI access (Sprint 5).

Users who have NOT purchased any BlueTeamers course get a limited, free daily
allowance of AI messages through the floating assistant. Users who purchase any
course automatically unlock premium access: unlimited AI usage and the full
/chat AI Workspace.
"""

from app.freemium.models import (
    AccessDecision,
    AccessLevel,
    AccessStatus,
    FreemiumLimitExceeded,
    UsageState,
)
from app.freemium.service import FreemiumService
from app.freemium.store import FreemiumStore

__all__ = [
    "AccessDecision",
    "AccessLevel",
    "AccessStatus",
    "FreemiumLimitExceeded",
    "UsageState",
    "FreemiumService",
    "FreemiumStore",
]
