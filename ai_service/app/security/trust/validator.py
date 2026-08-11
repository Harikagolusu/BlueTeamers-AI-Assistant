from typing import Any
from app.security.interfaces.i_trust import ITrustValidator, ISignatureValidator, ICertificateValidator
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class TrustValidationFailedEvent(AgentEvent):
    type: str = "TrustValidationFailed"
    entity_id: str
    reason: str

class TrustValidator(ITrustValidator):
    def __init__(self, signature_validator: ISignatureValidator, cert_validator: ICertificateValidator):
        self._signature_validator = signature_validator
        self._cert_validator = cert_validator

    def validate_trust(self, package: Any) -> bool:
        try:
            if not self._signature_validator.validate_signature(package):
                raise ValueError("Invalid Signature")
                
            cert_id = getattr(package, "certificate_id", None)
            if cert_id and not self._cert_validator.validate_certificate(cert_id):
                raise ValueError("Invalid Certificate")
                
            return True
        except Exception as e:
            entity_id = getattr(package, "id", "unknown")
            agent_event_bus.publish(TrustValidationFailedEvent(session_id="sys", entity_id=entity_id, reason=str(e)))
            return False
