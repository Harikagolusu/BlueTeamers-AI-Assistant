import time
import logging

from app.core.config import settings
from app.core.logging import request_id_var

from app.prompt_builder.schemas import (
    PromptRequest, PromptPayload, PromptResponse, PromptTemplate
)
from app.prompt_builder.exceptions import (
    TemplateNotFoundException, TokenLimitExceededException
)
from app.prompt_builder.templates import TEMPLATES
from app.context.tokenizer import TokenEstimator

logger = logging.getLogger("app.prompt_builder.builder")

class PromptProcessingLogic:
    """
    Encapsulates template retrieval and prompt formatting logic.
    """
    @staticmethod
    def get_template(name: str) -> PromptTemplate:
        template = TEMPLATES.get(name)
        if not template:
            raise TemplateNotFoundException(f"Template '{name}' not found.")
        return template

    @staticmethod
    def construct_payload(query: str, context_text: str, template: PromptTemplate) -> PromptPayload:
        if not context_text:
            context_text = "No context retrieved."
            
        user_formatted = template.user_prompt_template.format(
            context=context_text,
            query=query
        )
        
        return PromptPayload(
            system=template.system_prompt,
            user=user_formatted
        )
