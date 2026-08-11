import time
import logging
from app.prompt_builder.base import BasePromptBuilder
from app.prompt_builder.schemas import PromptRequest, PromptResponse, PromptPayload, HealthResponse
from app.context.tokenizer import TokenEstimator
from app.prompts.manager import PromptManager

logger = logging.getLogger(__name__)

class PromptAdapter(BasePromptBuilder):
    """
    Adapter bridging the legacy PromptBuilder interface to the new PromptManager.
    Ensures backward compatibility while supporting advanced prompt features.
    """
    def __init__(self, prompt_manager: PromptManager):
        self.prompt_manager = prompt_manager

    def build_prompt(self, request: PromptRequest) -> PromptResponse:
        start_time = time.time()
        template_name = request.template_name or "default_rag"
        
        # Determine format kwargs
        context_text = request.context.formatted_text if request.context and request.context.formatted_text else "No context retrieved."
        kwargs = {
            "query": request.query,
            "context": context_text
        }
        
        # Render prompt
        system_prompt, user_prompt = self.prompt_manager.render(template_name, **kwargs)
        
        payload = PromptPayload(system=system_prompt, user=user_prompt)
        
        sys_tokens = TokenEstimator.estimate_tokens(payload.system)
        user_tokens = TokenEstimator.estimate_tokens(payload.user)
        total_tokens = sys_tokens + user_tokens
        
        process_ms = (time.time() - start_time) * 1000
        
        return PromptResponse(
            payload=payload,
            estimated_tokens=total_tokens,
            processing_time_ms=process_ms,
            template_used=template_name
        )

    def health_check(self) -> HealthResponse:
        return HealthResponse(
            template_status="healthy",
            configuration_status="healthy"
        )
