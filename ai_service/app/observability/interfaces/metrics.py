from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseMetricsService(ABC):
    @abstractmethod
    def increment_counter(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter by value with specific labels."""
        pass

    @abstractmethod
    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Set a gauge to a specific value."""
        pass
        
    @abstractmethod
    def increment_gauge(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment a gauge by value."""
        pass
        
    @abstractmethod
    def decrement_gauge(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """Decrement a gauge by value."""
        pass

    @abstractmethod
    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        """Observe a value in a histogram."""
        pass

    @abstractmethod
    def get_registered_metrics_count(self) -> int:
        """Return the number of metrics registered."""
        pass
