import contextvars
from typing import Optional
from app.security.interfaces.i_context import ISecurityContextProvider
from app.security.context.security_context import SecurityContext

_security_context_var: contextvars.ContextVar[Optional[SecurityContext]] = contextvars.ContextVar(
    'security_context', default=None
)

class ContextProvider(ISecurityContextProvider):
    def get_context(self) -> SecurityContext:
        ctx = _security_context_var.get()
        if ctx is None:
            # Fallback to anonymous if not set, avoiding hard crashes for background tasks
            return SecurityContext.anonymous()
        return ctx

    def set_context(self, context: SecurityContext) -> None:
        _security_context_var.set(context)

    def clear_context(self) -> None:
        _security_context_var.set(None)
