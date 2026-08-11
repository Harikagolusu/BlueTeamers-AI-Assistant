import contextvars
from typing import Optional
from app.observability.context.observability_context import ObservabilityContext

_observability_context_var: contextvars.ContextVar[Optional[ObservabilityContext]] = contextvars.ContextVar(
    'observability_context', default=None
)

class ObservabilityContextProvider:
    def get_context(self) -> ObservabilityContext:
        ctx = _observability_context_var.get()
        if ctx is None:
            # Fallback to prevent background task crashes
            return ObservabilityContext.create_empty()
        return ctx

    def set_context(self, context: ObservabilityContext) -> None:
        _observability_context_var.set(context)

    def clear_context(self) -> None:
        _observability_context_var.set(None)
