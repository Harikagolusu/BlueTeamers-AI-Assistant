from typing import Any
from app.observability.interfaces.i_alerts import IAlertRule
from app.observability.models.alerts import Alert
import uuid

class HighLatencyRule(IAlertRule):
    def __init__(self, threshold_ms: float = 1000):
        self._threshold = threshold_ms

    def evaluate(self, metrics: Any) -> Alert | None:
        for m in metrics:
            if m.name == "http_request_duration_ms" and m.value > self._threshold:
                return Alert(
                    alert_id=str(uuid.uuid4()),
                    rule_name="HighLatencyRule",
                    severity="HIGH",
                    message=f"Request duration {m.value}ms exceeded {self._threshold}ms",
                    metadata=m.tags
                )
        return None

class ErrorSpikeRule(IAlertRule):
    def evaluate(self, metrics: Any) -> Alert | None:
        for m in metrics:
            if m.name == "http_requests_active" and m.tags.get("status") == "FAILED" and m.value > 10:
                return Alert(
                    alert_id=str(uuid.uuid4()),
                    rule_name="ErrorSpikeRule",
                    severity="CRITICAL",
                    message=f"Spike in error rate detected: {m.value} active failures."
                )
        return None
