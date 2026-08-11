from app.chat.intent.interfaces import IIntentPolicy
from app.chat.intent.pipeline.context import IntentPipelineContext
from app.chat.intent.models.clarification import ClarificationRequest

class AmbiguityPolicy(IIntentPolicy):
    """Detects ambiguous queries and flags them for clarification."""
    
    async def apply(self, context: IntentPipelineContext) -> IntentPipelineContext:
        if not context.candidate_intents:
            return context
            
        primary = context.candidate_intents[0]
        
        # Rule: If the best intent has very low confidence, it's ambiguous
        if primary.confidence < 0.3:
            return context.copy_with(
                clarification_request=ClarificationRequest(
                    reason="Low confidence in intent detection.",
                    suggested_prompt="Could you provide more specific details about what you want to do?",
                    missing_information=["Specific action or entity"]
                )
            )
            
        import re
        ambiguous_terms = ["it", "this", "that one", "him", "her"]
        # Remove punctuation for matching
        clean_query = re.sub(r'[^\w\s]', '', context.query.lower())
        query_words = clean_query.split()
        
        # Only trigger ambiguity if the query is very short (missing context)
        if len(query_words) <= 4 and any(term in query_words for term in ambiguous_terms) and not context.conversation_context:
            return context.copy_with(
                clarification_request=ClarificationRequest(
                    reason="Ambiguous reference detected without prior conversation context.",
                    suggested_prompt="What exactly are you referring to?",
                    missing_information=["Specific target reference"]
                )
            )
            
        return context
