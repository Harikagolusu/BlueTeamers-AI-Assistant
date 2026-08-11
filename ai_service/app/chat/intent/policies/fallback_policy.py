from app.chat.intent.interfaces import IIntentPolicy
from app.chat.intent.pipeline.context import IntentPipelineContext
from app.chat.intent.models.recommendations import ExecutionRecommendation
from app.chat.intent.models.intent_types import ExecutionMode

class FallbackPolicy(IIntentPolicy):
    """Provides fallback recommendations if the intent is unknown or missing."""
    
    async def apply(self, context: IntentPipelineContext) -> IntentPipelineContext:
        if context.clarification_request:
            # Already handled by ambiguity policy
            return context
            
        if not context.candidate_intents:
            # No intents generated at all (shouldn't happen with our rule classifier, but good practice)
            return context.copy_with(
                execution_recommendation=ExecutionRecommendation(
                    action="FALLBACK_GENERAL",
                    description="No intent could be determined. Defaulting to general chat."
                )
            )
            
        return context
