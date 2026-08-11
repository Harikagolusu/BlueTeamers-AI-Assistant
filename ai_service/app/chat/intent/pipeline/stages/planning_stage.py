from app.chat.intent.pipeline.i_intent_stage import IIntentPipelineStage
from app.chat.intent.pipeline.context import IntentPipelineContext
from app.chat.intent.interfaces import IExecutionPlanner

class ExecutionPlanningStage(IIntentPipelineStage):
    def __init__(self, planner: IExecutionPlanner):
        self._planner = planner

    @property
    def name(self) -> str:
        return "ExecutionPlanning"

    async def execute(self, context: IntentPipelineContext) -> IntentPipelineContext:
        return await self._planner.plan(context)
