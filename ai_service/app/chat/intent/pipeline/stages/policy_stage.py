from typing import List
from app.chat.intent.pipeline.i_intent_stage import IIntentPipelineStage
from app.chat.intent.pipeline.context import IntentPipelineContext
from app.chat.intent.interfaces import IIntentPolicy

class PolicyEvaluationStage(IIntentPipelineStage):
    def __init__(self, policies: List[IIntentPolicy]):
        self._policies = policies

    @property
    def name(self) -> str:
        return "PolicyEvaluation"

    async def execute(self, context: IntentPipelineContext) -> IntentPipelineContext:
        current_context = context
        for policy in self._policies:
            current_context = await policy.apply(current_context)
        return current_context
