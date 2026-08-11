from abc import ABC, abstractmethod
from typing import Callable, Any

class IMessageBus(ABC):
    @abstractmethod
    def publish(self, message: Any) -> None:
        """
        Publishes a message to the bus.
        """
        pass

    @abstractmethod
    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        """
        Subscribes a handler to a specific message type.
        """
        pass
