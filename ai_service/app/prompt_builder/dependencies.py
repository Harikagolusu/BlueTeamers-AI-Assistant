from app.prompt_builder.service import PromptBuilderService
from app.prompt_builder.base import BasePromptBuilder

_service_instance = PromptBuilderService()

def get_prompt_builder() -> BasePromptBuilder:
    """
    Dependency injection for the Prompt Builder layer.
    """
    return _service_instance
