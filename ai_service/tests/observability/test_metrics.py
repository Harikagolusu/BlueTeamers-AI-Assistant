import pytest
from app.observability.metrics.collector import InMemoryMetricsCollector
from app.observability.metrics.aggregator import MetricsAggregator
from app.observability.metrics.registry import InMemoryMetricsRegistry

def test_metrics_collection_and_aggregation():
    agg = MetricsAggregator()
    reg = InMemoryMetricsRegistry(agg)
    col = InMemoryMetricsCollector(reg)
    
    col.increment_counter("requests", 1, {"status": "ok"})
    col.increment_counter("requests", 2, {"status": "ok"})
    col.set_gauge("active", 5)
    
    metrics = reg.get_metrics()
    assert len(metrics) == 2
    
    # Aggregated counter
    req_metric = next(m for m in metrics if m.name == "requests")
    assert req_metric.value == 3
    
    act_metric = next(m for m in metrics if m.name == "active")
    assert act_metric.value == 5
