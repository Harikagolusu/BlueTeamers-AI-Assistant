from typing import Dict, Any, List, Tuple
import asyncio
import time
from app.runtime.interfaces.governance import IRateLimiter, IQuotaManager, IFeatureFlagService, IAuditLogger

class SlidingWindowRateLimiter(IRateLimiter):
    def __init__(self, requests_per_minute: int = 60, window_seconds: int = 60):
        self.rpm = requests_per_minute
        self.window_seconds = window_seconds
        # user_id:endpoint -> list of request timestamps (sliding window)
        self._timestamps: Dict[str, List[float]] = {}

    async def check_limit(self, user_id: str, endpoint: str) -> bool:
        now = time.monotonic()
        cutoff = now - self.window_seconds
        key = f"{user_id}:{endpoint}"
        timestamps = self._timestamps.setdefault(key, [])
        # Drop timestamps outside the current window.
        self._timestamps[key] = [ts for ts in timestamps if ts > cutoff]
        if len(self._timestamps[key]) >= self.rpm:
            return False
        self._timestamps[key].append(now)
        return True

    def reset(self) -> None:
        """Clear all rate-limit state (used by tests)."""
        self._timestamps.clear()

class DailyQuotaManager(IQuotaManager):
    def __init__(self, daily_token_limit: int = 100000):
        self.daily_limit = daily_token_limit
        self._usage: Dict[str, int] = {}
        
    async def check_quota(self, user_id: str) -> bool:
        return self._usage.get(user_id, 0) < self.daily_limit
        
    async def increment_usage(self, user_id: str, tokens: int) -> None:
        current = self._usage.get(user_id, 0)
        self._usage[user_id] = current + tokens

class ConfigFeatureFlagService(IFeatureFlagService):
    def __init__(self):
        self._flags = {
            "enable_streaming": True,
            "enable_cache": True,
            "enable_tool_calling": True,
            "enable_rag": True
        }
        
    async def is_enabled(self, feature_name: str, context: Dict[str, Any] = None) -> bool:
        return self._flags.get(feature_name, False)

class StructuredAuditLogger(IAuditLogger):
    async def log_event(self, event_type: str, user_id: str, details: Dict[str, Any]) -> None:
        # In an enterprise system, write to a compliance log like Splunk or Datadog
        print(f"[AUDIT] {event_type} by {user_id}: {details}")

class RuntimeGovernanceService:
    """
    Facade for all governance activities.
    """
    def __init__(
        self, 
        rate_limiter: IRateLimiter, 
        quota_manager: IQuotaManager, 
        feature_flags: IFeatureFlagService,
        audit_logger: IAuditLogger
    ):
        self.rate_limiter = rate_limiter
        self.quota_manager = quota_manager
        self.feature_flags = feature_flags
        self.audit_logger = audit_logger
