from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IRoleManager(ABC):
    @abstractmethod
    def get_roles(self, principal: str) -> List[str]: pass

class IPermissionManager(ABC):
    @abstractmethod
    def get_permissions(self, role: str) -> List[str]: pass

class IAccessEvaluator(ABC):
    @abstractmethod
    def evaluate_rbac(self, principal: str, required_permission: str) -> bool: pass
    @abstractmethod
    def evaluate_abac(self, principal: str, resource: Dict[str, Any], action: str) -> bool: pass

class IAuthorizationService(ABC):
    @abstractmethod
    def authorize(self, context: Any, required_permission: str, resource: Any = None) -> bool: pass
