from app.prompt_builder.schemas import HealthResponse
from app.prompt_builder.service import PromptBuilderService

def get_prompt_builder_health(service: PromptBuilderService) -> HealthResponse:
    return service.health_check()
