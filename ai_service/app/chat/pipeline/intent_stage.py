from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.chat.intent.interfaces import IIntentService

class IntentAnalysisStage(IExecutionStage):
    """Analyzes the user's intent to decide between GENERAL, RAG, or TOOL."""
    
    def __init__(self, intent_service: IIntentService):
        self._intent_service = intent_service
        
    @property
    def name(self) -> str:
        return "IntentAnalysis"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if "execution_result" in context.metadata:
            return context
            
        # Execute the Intent Intelligence subsystem
        query = context.metadata.get("query", "")
        # Build conversation context from memory if available, plus any attached
        # images/files so the classifier's attachment branch can fire.
        convo_context = {}
        if context.memory:
            convo_context["memory"] = context.memory
        if context.metadata.get("images"):
            convo_context["images"] = context.metadata["images"]
        if context.metadata.get("files"):
            convo_context["files"] = context.metadata["files"]
            
        analysis_result = await self._intent_service.analyze_intent(query, convo_context)
            
        # Store in metadata as a temporary compatibility choice 
        # to respect the ExecutionContext immutability freeze.
        new_metadata = {
            **context.metadata, 
            "intent_analysis": analysis_result,
            # Maintain legacy 'intent' property just in case other modules depend on it directly
            "intent": analysis_result.primary_intent.type.value
        }
        return context.model_copy(update={"metadata": new_metadata})
