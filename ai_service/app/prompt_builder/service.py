import time
import logging

from app.core.config import settings
from app.core.logging import request_id_var

from app.prompt_builder.base import BasePromptBuilder
from app.prompt_builder.builder import PromptProcessingLogic
from app.prompt_builder.schemas import PromptRequest, PromptResponse, HealthResponse
from app.context.tokenizer import TokenEstimator

logger = logging.getLogger("app.prompt_builder.service")

class PromptBuilderService(BasePromptBuilder):
    """
    Orchestrates Prompt Construction.
    Does not call LLMs.
    """
    def __init__(self):
        self.max_prompt_tokens = getattr(settings, "MAX_PROMPT_TOKENS", 8000)

    def build_prompt(self, request: PromptRequest) -> PromptResponse:
        start_time = time.time()
        req_id = request_id_var.get() if request_id_var.get() != "-" else "sys"
        
        template_name = request.template_name or "default_rag"
        logger.info(f"Prompt Builder Start - Template: {template_name} - ReqID: {req_id}")

        # 1. Fetch Template
        template = PromptProcessingLogic.get_template(template_name)
        
        # 2. Build Payload
        payload = PromptProcessingLogic.construct_payload(
            query=request.query,
            context_text=request.context.formatted_text,
            template=template
        )
        
        # 3. Estimate Tokens
        sys_tokens = TokenEstimator.estimate_tokens(payload.system)
        user_tokens = TokenEstimator.estimate_tokens(payload.user)
        total_tokens = sys_tokens + user_tokens
        
        if total_tokens > self.max_prompt_tokens:
            logger.warning(
                f"Prompt exceeds max tokens limits! Estimated: {total_tokens}, Max: {self.max_prompt_tokens}"
            )
            
        process_ms = (time.time() - start_time) * 1000
        
        logger.info(
            f"Prompt Builder Complete - Template: {template_name} - Tokens: {total_tokens} - "
            f"Context Chunks: {len(request.context.chunks)} - Latency: {process_ms:.2f}ms - ReqID: {req_id}"
        )

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
