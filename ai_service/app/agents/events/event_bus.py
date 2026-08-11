from typing import Callable, List, Dict
import asyncio
import logging
from app.agents.events.agent_events import AgentEvent

logger = logging.getLogger(__name__)

class EventBus:
    """Internal publish/subscribe event bus for agent lifecycle events."""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[AgentEvent], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[AgentEvent], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event: AgentEvent):
        logger.info(f"EventBus publishing: {event.type} for session {event.session_id}")
        handlers = self._subscribers.get(event.type, [])
        for handler in handlers:
            try:
                # If async handler
                import inspect
                if inspect.iscoroutinefunction(handler):
                    asyncio.create_task(handler(event))
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error in event handler for {event.type}: {str(e)}")

# Singleton instance for the agent subsystem
agent_event_bus = EventBus()
