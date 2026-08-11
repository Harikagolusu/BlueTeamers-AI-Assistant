from abc import ABC, abstractmethod
from typing import Dict, Any

class IRateLimiter(ABC):
    @abstractmethod
    async def check_limit(self, user_id: str, endpoint: str) -> bool:
        """Returns True if request is allowed, False if throttled."""
        pass

class IQuotaManager(ABC):
    @abstractmethod
    async def check_quota(self, user_id: str) -> bool:
        """Returns True if quota is available, False if exhausted."""
        pass
        
    @abstractmethod
    async def increment_usage(self, user_id: str, tokens: int) -> None:
        pass

class IFeatureFlagService(ABC):
    @abstractmethod
    async def is_enabled(self, feature_name: str, context: Dict[str, Any] = None) -> bool:
        pass

class IAuditLogger(ABC):
    @abstractmethod
    async def log_event(self, event_type: str, user_id: str, details: Dict[str, Any]) -> None:
        """Structured audit logging without sensitive prompt data."""
        pass

class IHealthMonitor(ABC):
    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """Aggregate health across dependencies."""
        pass

class IDiagnosticService(ABC):
    @abstractmethod
    async def validate_startup(self) -> bool:
        pass
