from abc import ABC, abstractmethod
from typing import Any

class IQuotaManager(ABC):
    @abstractmethod
    def check_quota(self, tenant_id: str, resource: str, amount: int) -> bool: pass
    @abstractmethod
    def consume_quota(self, tenant_id: str, resource: str, amount: int) -> None: pass

class IBudgetManager(ABC):
    @abstractmethod
    def check_budget(self, tenant_id: str, cost: float) -> bool: pass
    @abstractmethod
    def consume_budget(self, tenant_id: str, cost: float) -> None: pass

class IRestrictionManager(ABC):
    @abstractmethod
    def is_allowed(self, tenant_id: str, entity_type: str, entity_id: str) -> bool: pass

class IGovernanceService(ABC):
    @abstractmethod
    def enforce_governance(self, context: Any, request: Any) -> None: pass
