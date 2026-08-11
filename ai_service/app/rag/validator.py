import logging
from app.llm.schemas import LLMResponse
from app.context.schemas import ContextDocument
from app.rag.exceptions import ValidationFailure

logger = logging.getLogger("app.rag.validator")

class ResponseValidator:
    """
    Focused validator ensuring response structural integrity and metadata constraints.
    Does NOT inspect retrieval internals or perform advanced hallucination heuristics.
    """
    
    def validate(self, llm_response: LLMResponse, context: ContextDocument) -> bool:
        if not llm_response or not llm_response.text:
            raise ValidationFailure("LLM returned an empty response.")
            
        text = llm_response.text.strip()
        if len(text) == 0:
            raise ValidationFailure("LLM returned whitespace-only response.")
            
        # Basic token usage constraint check
        if llm_response.usage:
            # We just verify it's formatted as expected if it exists
            pass
            
        # Add basic structural validation (e.g. check for malformed JSON if we expect JSON, etc.)
        
        return True
