from abc import ABC, abstractmethod
from typing import Dict, Any

class IExecutionTimeline(ABC):
    @abstractmethod
    def add_event(self, timestamp: str, event_type: str, details: Dict[str, Any]) -> None: pass
    @abstractmethod
    def generate(self) -> list: pass

class IDiagnosticsAnalyzer(ABC):
    @abstractmethod
    def create_snapshot(self, context: Any) -> Dict[str, Any]: pass
