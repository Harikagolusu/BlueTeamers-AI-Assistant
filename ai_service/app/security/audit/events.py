from app.agents.events.agent_events import AgentEvent
from typing import Dict, Any

class AuditRecordCreatedEvent(AgentEvent):
    type: str = "AuditRecordCreated"
    audit_id: str
    action: str
    principal: str
    resource: str
