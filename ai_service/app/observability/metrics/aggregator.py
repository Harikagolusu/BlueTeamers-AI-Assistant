from app.observability.interfaces.i_metrics import IMetricsAggregator

class MetricsAggregator(IMetricsAggregator):
    def aggregate(self, metrics_batch: list) -> list:
        # Example: Aggregate counters with same name/tags in batch
        aggregated = {}
        for m in metrics_batch:
            key = (m.name, m.type, frozenset(m.tags.items()))
            if key not in aggregated:
                aggregated[key] = m
            else:
                if m.type == "counter":
                    aggregated[key].value += m.value
                elif m.type == "gauge":
                    aggregated[key].value = m.value # Keep latest gauge
                else:
                    # Append or avg histograms (stubbed)
                    pass
        return list(aggregated.values())
