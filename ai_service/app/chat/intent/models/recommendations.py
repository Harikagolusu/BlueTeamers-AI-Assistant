from pydantic import BaseModel
from typing import Optional
from app.chat.intent.models.intent_types import ExecutionMode

class RouteRecommendation(BaseModel):
    engine: str
    confidence: float
    reasoning: str
    execution_mode: ExecutionMode

class ExecutionRecommendation(BaseModel):
    action: str
    description: str
    # Future agentic capabilities can add sub-steps, tools, etc. here.
