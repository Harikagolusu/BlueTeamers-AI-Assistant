from pydantic import BaseModel
from typing import Dict, Any, Optional

from app.context.schemas import ContextDocument

class PromptRequest(BaseModel):
    query: str
    context: ContextDocument
    template_name: Optional[str] = "default_rag"

class PromptTemplate(BaseModel):
    name: str
    system_prompt: str
    user_prompt_template: str

class PromptPayload(BaseModel):
    """The final constructed text payload ready for the LLM."""
    system: str
    user: str

class PromptResponse(BaseModel):
    payload: PromptPayload
    estimated_tokens: int
    processing_time_ms: float
    template_used: str

class HealthResponse(BaseModel):
    template_status: str
    configuration_status: str
