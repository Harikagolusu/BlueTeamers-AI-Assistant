from abc import ABC, abstractmethod
from typing import Dict, Any

class IAlertRule(ABC):
    @abstractmethod
    def evaluate(self, metrics: Any) -> bool: pass

class INotifier(ABC):
    @abstractmethod
    async def notify(self, alert: Any) -> None: pass

class IAlertManager(ABC):
    @abstractmethod
    def register_rule(self, rule: IAlertRule) -> None: pass
    @abstractmethod
    def process_alerts(self, metrics: Any) -> None: pass
