import time
from typing import Callable, Any
from app.observability.context.context_provider import ObservabilityContextProvider
from app.observability.context.observability_context import ObservabilityContext
from app.observability.instrumentation.facade import InstrumentationFacade
from app.agents.events.event_bus import agent_event_bus
from app.agents.events.agent_events import AgentEvent

class RequestStartedEvent(AgentEvent):
    type: str = "RequestStarted"
    correlation_id: str

class RequestCompletedEvent(AgentEvent):
    type: str = "RequestCompleted"
    correlation_id: str
    duration_ms: float
    status: str

class ObservabilityMiddleware:
    def __init__(self, facade: InstrumentationFacade, context_provider: ObservabilityContextProvider):
        self._facade = facade
        self._context_provider = context_provider

    async def execute(self, request: Any, next_handler: Callable) -> Any:
        ctx = ObservabilityContext()
        self._context_provider.set_context(ctx)
        
        agent_event_bus.publish(RequestStartedEvent(
            session_id=ctx.tenant,
            correlation_id=ctx.correlation_id
        ))
        
        self._facade.increment_counter("http_requests_active", 1)
        start_time = time.perf_counter()
        
        try:
            span = self._facade.start_span(name="business_pipeline", parent_id=None)
            self._facade.log_info("Request Started", correlation_id=ctx.correlation_id)
            
            # Delegate to inner pipeline (e.g., Security Middleware)
            response = await next_handler(request)
            
            status = "SUCCESS"
            return response
        except Exception as e:
            status = "FAILED"
            self._facade.log_error("Request Failed", error=str(e), correlation_id=ctx.correlation_id)
            raise
        finally:
            span.end()
            duration = (time.perf_counter() - start_time) * 1000
            self._facade.record_latency("http_request_duration_ms", duration, {"status": status})
            self._facade.increment_counter("http_requests_active", -1)
            
            agent_event_bus.publish(RequestCompletedEvent(
                session_id=ctx.tenant,
                correlation_id=ctx.correlation_id,
                duration_ms=duration,
                status=status
            ))
            
            self._context_provider.clear_context()
