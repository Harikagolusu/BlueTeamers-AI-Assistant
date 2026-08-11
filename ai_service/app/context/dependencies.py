from app.context.service import ContextBuilderService
from app.context.base import BaseContextBuilder

_service_instance = ContextBuilderService()

def get_context_builder() -> BaseContextBuilder:
    """
    Dependency injection for the ContextBuilder layer.
    """
    return _service_instance
