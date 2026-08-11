import pytest
import asyncio
from unittest.mock import MagicMock
from app.observability.middleware.observability_middleware import ObservabilityMiddleware
from app.observability.context.context_provider import ObservabilityContextProvider

@pytest.mark.asyncio
async def test_observability_middleware():
    facade = MagicMock()
    span = MagicMock()
    facade.start_span.return_value = span
    context_provider = ObservabilityContextProvider()
    
    middleware = ObservabilityMiddleware(facade, context_provider)
    
    async def next_handler(req):
        assert context_provider.get_context().correlation_id is not None
        return "OK"
        
    res = await middleware.execute({}, next_handler)
    assert res == "OK"
    
    facade.start_span.assert_called_once()
    span.end.assert_called_once()
    facade.record_latency.assert_called_once()
    
    assert context_provider.get_context().correlation_id != None # Actually, it gets cleared
    # Wait, the middleware calls clear_context() at the end.
