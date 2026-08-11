import uuid
from typing import Dict, Optional
from contextvars import ContextVar

from app.observability.interfaces.tracing import BaseTracingService

# Context variables for distributed tracing
trace_id_var: ContextVar[Optional[str]] = ContextVar("trace_id", default=None)
span_id_var: ContextVar[Optional[str]] = ContextVar("span_id", default=None)

class NativeTracingAdapter(BaseTracingService):
    """
    Native implementation of W3C-compatible tracing using ContextVars.
    """
    
    def set_trace_context(self, trace_id: str, span_id: str) -> None:
        trace_id_var.set(trace_id)
        span_id_var.set(span_id)

    def get_trace_context(self) -> Dict[str, Optional[str]]:
        return {
            "trace_id": trace_id_var.get(),
            "span_id": span_id_var.get()
        }

    def generate_trace_id(self) -> str:
        """Generate a 32-character hex W3C trace ID."""
        return uuid.uuid4().hex

    def generate_span_id(self) -> str:
        """Generate a 16-character hex W3C span ID."""
        return uuid.uuid4().hex[:16]
