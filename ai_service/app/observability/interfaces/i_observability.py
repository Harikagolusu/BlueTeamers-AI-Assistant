from abc import ABC, abstractmethod
from typing import Dict, Any

class IObservabilityService(ABC):
    @abstractmethod
    def log_execution(self, trace_id: str, metadata: Dict[str, Any]) -> None:
        """Log pipeline execution telemetry."""
        pass
        
    @abstractmethod
    def log_error(self, trace_id: str, error: Exception) -> None:
        """Log pipeline execution error."""
        pass
