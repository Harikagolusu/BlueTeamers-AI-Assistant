from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.chat.intent.models.entities import EntityCollection
from app.chat.intent.models.analysis_result import DetectedIntent
from app.chat.intent.models.clarification import ClarificationRequest
from app.chat.intent.models.recommendations import RouteRecommendation, ExecutionRecommendation

class IntentPipelineContext(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    query: str
    conversation_context: Dict[str, Any] = Field(default_factory=dict)
    
    # State accumulated by stages
    entities: EntityCollection = Field(default_factory=EntityCollection)
    candidate_intents: List[DetectedIntent] = Field(default_factory=list)
    clarification_request: Optional[ClarificationRequest] = None
    
    route_recommendation: Optional[RouteRecommendation] = None
    execution_recommendation: Optional[ExecutionRecommendation] = None
    
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def copy_with(self, **kwargs) -> 'IntentPipelineContext':
        """Pydantic V2 copy wrapper to handle immutability updates cleanly"""
        return self.model_copy(update=kwargs)
