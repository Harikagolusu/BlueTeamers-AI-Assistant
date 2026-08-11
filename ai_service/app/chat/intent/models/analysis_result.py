from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.chat.intent.models.intent_types import IntentType
from app.chat.intent.models.entities import EntityCollection
from app.chat.intent.models.clarification import ClarificationRequest
from app.chat.intent.models.recommendations import RouteRecommendation, ExecutionRecommendation

class DetectedIntent(BaseModel):
    type: IntentType
    confidence: float
    reason: str
    matched_features: List[str] = Field(default_factory=list)

class IntentAnalysisResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    primary_intent: DetectedIntent
    secondary_intents: List[DetectedIntent] = Field(default_factory=list)
    
    entities: EntityCollection = Field(default_factory=EntityCollection)
    conversation_context: Dict[str, Any] = Field(default_factory=dict)
    
    clarification_request: Optional[ClarificationRequest] = None
    
    route_recommendation: Optional[RouteRecommendation] = None
    execution_recommendation: Optional[ExecutionRecommendation] = None
