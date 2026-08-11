from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

class ISharedMemory(ABC):
    @abstractmethod
    def read(self, key: str, namespace: str = "default") -> Optional[Any]:
        pass

    @abstractmethod
    def write(self, key: str, value: Any, namespace: str = "default") -> None:
        pass

    @abstractmethod
    def get_namespace(self, namespace: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def create_snapshot(self) -> str:
        pass

    @abstractmethod
    def restore_snapshot(self, snapshot_id: str) -> None:
        pass
