from typing import Any
from app.security.interfaces.i_policy import IPolicyEnforcementPoint, IPolicyDecisionPoint
from app.security.context.security_context import SecurityContext
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class PolicyViolationDetectedEvent(AgentEvent):
    type: str = "PolicyViolationDetected"
    principal: str
    resource: str
    action: str

class PolicyEnforcementPoint(IPolicyEnforcementPoint):
    def __init__(self, pdp: IPolicyDecisionPoint):
        self._pdp = pdp

    def enforce(self, context: SecurityContext, resource: Any, action: str) -> None:
        if not self._pdp.evaluate_access(context, resource, action):
            agent_event_bus.publish(PolicyViolationDetectedEvent(
                session_id=context.session or "unknown",
                principal=context.principal,
                resource=str(resource),
                action=action
            ))
            raise PermissionError(f"Policy Engine denied action {action} on resource.")
