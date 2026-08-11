from abc import ABC, abstractmethod
from typing import Dict, Any, List

class IAuditLogger(ABC):
    @abstractmethod
    def log_event(self, action: str, resource: str, result: str, metadata: Dict[str, Any] = None) -> None: pass

class IAuditRepository(ABC):
    @abstractmethod
    def save(self, record: Any) -> None: pass
    @abstractmethod
    def query(self, filters: Dict[str, Any]) -> List[Any]: pass
