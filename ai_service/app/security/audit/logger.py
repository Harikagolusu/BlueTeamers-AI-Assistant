from typing import Dict, Any
from app.security.interfaces.i_audit import IAuditLogger, IAuditRepository
from app.security.models.audit_record import AuditRecord
from app.security.context.security_context import SecurityContext
from app.agents.events.event_bus import agent_event_bus
from app.security.audit.events import AuditRecordCreatedEvent

class AuditLogger(IAuditLogger):
    def __init__(self, repository: IAuditRepository, context_provider: Any):
        self._repository = repository
        self._context_provider = context_provider

    def log_event(self, action: str, resource: str, result: str, metadata: Dict[str, Any] = None) -> None:
        ctx: SecurityContext = self._context_provider.get_context()
        record = AuditRecord(
            principal=ctx.principal,
            correlation_id=ctx.correlation_id,
            action=action,
            resource=resource,
            result=result,
            metadata=metadata or {}
        )
        self._repository.save(record)
        
        agent_event_bus.publish(AuditRecordCreatedEvent(
            session_id=ctx.session or "sys",
            audit_id=record.audit_id,
            action=record.action,
            principal=record.principal,
            resource=record.resource
        ))
