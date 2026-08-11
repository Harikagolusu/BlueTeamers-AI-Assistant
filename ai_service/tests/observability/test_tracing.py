import pytest
import asyncio
from unittest.mock import AsyncMock
from app.observability.tracing.tracer import ObservabilityTracer
from app.observability.tracing.sampling import PercentageSampler, AlwaysOnSampler
from app.observability.context.context_provider import ObservabilityContextProvider
from app.observability.context.observability_context import ObservabilityContext

@pytest.mark.asyncio
async def test_tracer_always_samples():
    provider = ObservabilityContextProvider()
    provider.set_context(ObservabilityContext())
    
    exporter = AsyncMock()
    sampler = AlwaysOnSampler()
    
    tracer = ObservabilityTracer(provider, exporter, sampler)
    span = tracer.start_span("test_span")
    
    span.set_attribute("key", "val")
    span.end()
    
    # Give async task time to run
    await asyncio.sleep(0.05)
    exporter.export.assert_called_once()
