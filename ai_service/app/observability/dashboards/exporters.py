import asyncio
from typing import Any
from app.observability.interfaces.i_dashboards import IExporter
from app.observability.interfaces.i_tracing import ITraceExporter

class PrometheusExporterStub(IExporter):
    async def export(self, data: Any) -> None:
        # Simulate pushing to Pushgateway or exposing /metrics
        await asyncio.sleep(0.01)

class GrafanaExporterStub(IExporter):
    async def export(self, data: Any) -> None:
        # Simulate pushing dashboard configs or loki logs
        await asyncio.sleep(0.01)

class OpenTelemetryTraceExporterStub(ITraceExporter):
    async def export(self, spans: list) -> None:
        # Simulate pushing OTLP spans
        await asyncio.sleep(0.01)
