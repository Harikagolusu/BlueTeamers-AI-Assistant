from abc import ABC, abstractmethod
from typing import Dict, Optional

class BaseTracingService(ABC):
    @abstractmethod
    def set_trace_context(self, trace_id: str, span_id: str) -> None:
        """Set the current trace and span ID in the context."""
        pass

    @abstractmethod
    def get_trace_context(self) -> Dict[str, Optional[str]]:
        """Return the current trace context (trace_id, span_id)."""
        pass

    @abstractmethod
    def generate_trace_id(self) -> str:
        """Generate a new W3C compliant trace ID."""
        pass

    @abstractmethod
    def generate_span_id(self) -> str:
        """Generate a new W3C compliant span ID."""
        pass
