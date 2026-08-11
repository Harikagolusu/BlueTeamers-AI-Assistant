from typing import Callable, Any
from app.agents.interfaces.i_message_bus import IMessageBus
from app.agents.events.event_bus import agent_event_bus

class MessageBusAdapter(IMessageBus):
    """
    Adapts the IMessageBus interface to use the existing agent_event_bus.
    This preserves telemetry and decoupled communication without building a new queue.
    """
    def publish(self, message: Any) -> None:
        agent_event_bus.publish(message)

    def subscribe(self, event_type: type, handler: Callable[[Any], None]) -> None:
        agent_event_bus.subscribe(event_type, handler)
