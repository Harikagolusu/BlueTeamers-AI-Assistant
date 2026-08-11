from abc import ABC, abstractmethod
from typing import Any, Dict, List

class IPolicyRegistry(ABC):
    @abstractmethod
    def get_policies(self, resource_type: str) -> List[Any]: pass

class IPolicyEvaluator(ABC):
    @abstractmethod
    def evaluate(self, policy: Any, context: Any) -> bool: pass

class IPolicyDecisionPoint(ABC):
    @abstractmethod
    def evaluate_access(self, context: Any, resource: Any, action: str) -> bool: pass

class IPolicyEnforcementPoint(ABC):
    @abstractmethod
    def enforce(self, context: Any, resource: Any, action: str) -> None: pass
