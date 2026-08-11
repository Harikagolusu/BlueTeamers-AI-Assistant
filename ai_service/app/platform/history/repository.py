from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class IExecutionHistoryRepository(ABC):
    """
    Interface for appending and querying execution history.
    """
    @abstractmethod
    def append_record(self, execution_id: str, state: str, metadata: Dict[str, Any]) -> None:
        pass
        
    @abstractmethod
    def get_history(self, execution_id: str) -> List[Dict[str, Any]]:
        pass
        
class InMemoryExecutionHistoryRepository(IExecutionHistoryRepository):
    def __init__(self):
        self._store: Dict[str, List[Dict[str, Any]]] = {}
        
    def append_record(self, execution_id: str, state: str, metadata: Dict[str, Any]) -> None:
        if execution_id not in self._store:
            self._store[execution_id] = []
        self._store[execution_id].append({
            "state": state,
            "metadata": metadata
        })
        
    def get_history(self, execution_id: str) -> List[Dict[str, Any]]:
        return self._store.get(execution_id, [])
