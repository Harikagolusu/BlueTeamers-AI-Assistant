import time
from typing import Callable, Awaitable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.observability.service import ObservabilityService

class ObservabilityMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle W3C distributed tracing and API metrics collection.
    """
    def __init__(self, app, observability_service: ObservabilityService):
        super().__init__(app)
        self.obs = observability_service

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Extract W3C Trace Context from headers if present
        traceparent = request.headers.get("traceparent")
        
        if traceparent and len(traceparent.split("-")) == 4:
            parts = traceparent.split("-")
            trace_id = parts[1]
            span_id = self.obs.generate_span_id()  # new span for this service boundary
        else:
            trace_id = self.obs.generate_trace_id()
            span_id = self.obs.generate_span_id()
            
        self.obs.set_trace_context(trace_id, span_id)
        
        # We also set request_id_var to span_id for legacy compatibility
        from app.core.logging import request_id_var
        request.state.request_id = span_id
        request_id_var.set(span_id)

        method = request.method
        path = request.url.path
        
        # Metrics: increment active requests
        labels = {"method": method, "endpoint": path}
        self.obs.increment_gauge("api_requests_active", 1.0, labels)
        
        start_time = time.time()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            
            # Inject trace ID back to client
            response.headers["X-Trace-ID"] = trace_id
            
            return response
        finally:
            duration = time.time() - start_time
            self.obs.decrement_gauge("api_requests_active", 1.0, labels)
            
            metrics_labels = {"method": method, "endpoint": path, "status": str(status_code)}
            self.obs.increment_counter("api_requests_total", 1.0, metrics_labels)
            self.obs.observe_histogram("api_request_duration_seconds", duration, metrics_labels)
            
            self.obs.log_info(
                f"API Request completed: {method} {path} - {status_code}",
                execution_time_ms=duration * 1000,
                status_code=status_code
            )
