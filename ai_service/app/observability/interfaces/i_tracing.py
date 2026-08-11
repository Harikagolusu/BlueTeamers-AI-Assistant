from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ISpan(ABC):
    @abstractmethod
    def set_attribute(self, key: str, value: Any) -> None: pass
    @abstractmethod
    def add_event(self, name: str, attributes: Dict[str, Any] = None) -> None: pass
    @abstractmethod
    def end(self) -> None: pass

class ITracer(ABC):
    @abstractmethod
    def start_span(self, name: str, parent_id: Optional[str] = None) -> ISpan: pass

class ITraceExporter(ABC):
    @abstractmethod
    async def export(self, spans: list) -> None: pass
