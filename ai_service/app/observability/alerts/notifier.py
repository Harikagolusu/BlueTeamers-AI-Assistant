import asyncio
from typing import Any
from app.observability.interfaces.i_alerts import INotifier
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent
from app.observability.models.alerts import Alert

class AlertRaisedEvent(AgentEvent):
    type: str = "AlertRaised"
    alert_id: str
    severity: str
    rule_name: str
    message: str

class AsyncNotifier(INotifier):
    async def notify(self, alert: Alert) -> None:
        # Offloads dispatch to EventBus so email/slack listeners can handle it
        await asyncio.to_thread(self._publish, alert)
        
    def _publish(self, alert: Alert):
        agent_event_bus.publish(AlertRaisedEvent(
            session_id="sys",
            alert_id=alert.alert_id,
            severity=alert.severity,
            rule_name=alert.rule_name,
            message=alert.message
        ))
