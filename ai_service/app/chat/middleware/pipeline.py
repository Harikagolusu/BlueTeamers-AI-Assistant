# Simulating application-level middleware components
# In FastAPI, these would be BaseHTTPMiddleware implementations

from app.chat.context.execution_context import ExecutionContext
from app.chat.exceptions.chat_exceptions import ValidationError
from app.security.base_interfaces import IGuardrailsService
from app.cache.interfaces import ICacheService

class ExceptionHandlingMiddleware:
    """Catches unhandled exceptions and maps them to standard BaseChatError schemas."""
    pass

class GuardrailsMiddleware:
    """Synchronous checks for Prompt Injection and PII before passing to the orchestrator."""
    def __init__(self, guardrails_service: IGuardrailsService):
        self._guardrails = guardrails_service

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        query = context.metadata.get("query", "")
        if not query:
            return context
            
        is_safe = await self._guardrails.validate(query)
        if not is_safe:
            raise ValidationError("Query blocked by security guardrails.")
        return context

from app.observability.interfaces.i_observability import IObservabilityService

class ObservabilityMiddleware:
    """Logs telemetry for the execution."""
    def __init__(self, observability: IObservabilityService):
        self._obs = observability

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        # Start timer here if we wanted to measure full duration
        # For now, just enrich the context
        return context

    async def post_execute(self, context: ExecutionContext, result=None, error=None) -> None:
        if error:
            self._obs.log_error(str(context.trace_id), error)
        if result:
            self._obs.log_execution(str(context.trace_id), {
                "latency_ms": getattr(result, "latency_ms", 0),
                "engine": getattr(result, "engine_name", "UNKNOWN"),
                "status": getattr(result, "status", "UNKNOWN")
            })

class RequestEnrichmentMiddleware:
    """Extracts JWT claims, tenant IDs, and Trace IDs to begin building the ExecutionContext."""
    pass
