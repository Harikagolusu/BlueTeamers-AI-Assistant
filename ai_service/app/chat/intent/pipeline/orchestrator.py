from typing import List
from app.chat.intent.pipeline.i_intent_stage import IIntentPipelineStage
from app.chat.intent.pipeline.context import IntentPipelineContext

class IntentOrchestrator:
    def __init__(self, stages: List[IIntentPipelineStage]):
        self._stages = stages

    async def execute_pipeline(self, context: IntentPipelineContext) -> IntentPipelineContext:
        current_context = context
        for stage in self._stages:
            current_context = await stage.execute(current_context)
            
            # Short-circuit logic if clarification is required early
            if current_context.clarification_request:
                # If ambiguity policy flagged clarification, we might not need to run execution planning
                # But it's safer to let the planner turn the clarification into a Deferred/Rejected recommendation.
                pass
                
        return current_context
