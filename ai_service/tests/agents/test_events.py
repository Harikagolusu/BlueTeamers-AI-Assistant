import pytest
import asyncio
from app.agents.events.event_bus import EventBus
from app.agents.events.agent_events import ExecutionStartedEvent

@pytest.mark.asyncio
async def test_event_bus():
    bus = EventBus()
    received = []
    
    def sync_handler(event):
        received.append(event)
        
    async def async_handler(event):
        received.append(event)
        
    bus.subscribe("ExecutionStarted", sync_handler)
    bus.subscribe("ExecutionStarted", async_handler)
    
    event = ExecutionStartedEvent(session_id="session1", plan_id="plan1")
    bus.publish(event)
    
    # Allow async handler to run
    await asyncio.sleep(0.01)
    
    assert len(received) == 2
    assert received[0].plan_id == "plan1"
