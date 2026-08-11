from typing import Dict, Any

class MetricsService:
    """
    Centralized metrics collection service.
    """
    def record_counter(self, name: str, value: int = 1, tags: Dict[str, str] = None) -> None:
        pass

    def record_gauge(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        pass

    def record_histogram(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        pass
