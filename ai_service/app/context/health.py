from app.context.service import ContextBuilderService

def get_context_health(service: ContextBuilderService) -> dict:
    return service.health_check()
