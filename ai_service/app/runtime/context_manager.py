import contextvars
from contextlib import contextmanager
from typing import Generator, Optional
from app.runtime.models.context import RuntimeContext

# ContextVar holding the current request's operational state
_runtime_context_var: contextvars.ContextVar[RuntimeContext] = contextvars.ContextVar('runtime_context')

class RuntimeContextManager:
    """
    Manages the lifecycle of the RuntimeContext across a request using contextvars.
    """
    
    @staticmethod
    def initialize(trace_id: str, session_id: Optional[str] = None, user_id: Optional[str] = None) -> contextvars.Token:
        """
        Request Starts -> RuntimeContext Created
        """
        ctx = RuntimeContext(
            trace_id=trace_id,
            session_id=session_id,
            user_id=user_id
        )
        return _runtime_context_var.set(ctx)
        
    @staticmethod
    def get() -> RuntimeContext:
        """
        Retrieve the current RuntimeContext. Raises LookupError if outside a request lifecycle.
        """
        return _runtime_context_var.get()
        
    @staticmethod
    def update(**kwargs) -> None:
        """
        Update the current RuntimeContext. Note: Pydantic V2 model_copy is used for immutability.
        Since we need to update the contextvar to point to the new instance, we do that here.
        """
        try:
            ctx = _runtime_context_var.get()
            new_ctx = ctx.model_copy(update=kwargs)
            _runtime_context_var.set(new_ctx)
        except LookupError:
            pass # Or log a warning if trying to update outside of lifecycle
            
    @staticmethod
    def dispose(token: contextvars.Token) -> None:
        """
        Telemetry Finalized -> Disposed
        """
        _runtime_context_var.reset(token)

    @staticmethod
    @contextmanager
    def lifecycle(trace_id: str, session_id: Optional[str] = None, user_id: Optional[str] = None) -> Generator[None, None, None]:
        """
        Convenience context manager for wrapping the entire lifecycle block.
        """
        token = RuntimeContextManager.initialize(trace_id, session_id, user_id)
        try:
            yield
        finally:
            RuntimeContextManager.dispose(token)
