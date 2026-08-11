import pytest
from app.observability.alerts.rules import HighLatencyRule, ErrorSpikeRule
from app.observability.models.metrics import MetricRecord

def test_high_latency_rule():
    rule = HighLatencyRule(threshold_ms=500)
    
    good_metric = MetricRecord(name="http_request_duration_ms", type="histogram", value=200)
    assert rule.evaluate([good_metric]) is None
    
    bad_metric = MetricRecord(name="http_request_duration_ms", type="histogram", value=600)
    alert = rule.evaluate([bad_metric])
    
    assert alert is not None
    assert alert.severity == "HIGH"
