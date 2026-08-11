import pytest
from app.planning.models.plan import ExecutionPlan, Capability, ExecutionPlanStatus
from app.planning.services.planning_service import PlanningService
from typing import Any, List
from pydantic import BaseModel, ConfigDict

class _MockType(BaseModel):
    name: str

    @property
    def value(self) -> str:
        return self.name

class _MockIntent(BaseModel):
    type: _MockType

class MockIntentAnalysis(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    clarification_request: bool = False
    secondary_intents: List[str] = []
    primary_intent: _MockIntent

    def __init__(self, clarification_request=False, secondary_intents=None, primary_type="GENERAL_CHAT"):
        super().__init__(
            clarification_request=clarification_request,
            secondary_intents=secondary_intents or [],
            primary_intent=_MockIntent(type=_MockType(name=primary_type))
        )

@pytest.mark.asyncio
async def test_single_planner():
    service = PlanningService()
    intent = MockIntentAnalysis(primary_type="KNOWLEDGE_RETRIEVAL")
    ctx = await service.create_plan(intent, {})
    
    assert ctx.plan is not None
    assert ctx.plan.status == ExecutionPlanStatus.READY
    assert len(ctx.plan.steps) == 1
    assert ctx.plan.steps[0].required_capability == Capability.RAG

@pytest.mark.asyncio
async def test_hybrid_planner():
    service = PlanningService()
    intent = MockIntentAnalysis(secondary_intents=["OTHER_INTENT"])
    ctx = await service.create_plan(intent, {})
    
    assert len(ctx.plan.steps) == 3
    assert ctx.plan.steps[0].required_capability == Capability.RAG
    assert ctx.plan.steps[1].required_capability == Capability.TOOL
    assert ctx.plan.steps[2].required_capability == Capability.LLM
    # Validate graph dependencies
    assert ctx.plan.steps[1].dependencies == [ctx.plan.steps[0].step_id]
    assert ctx.plan.steps[2].dependencies == [ctx.plan.steps[1].step_id]

@pytest.mark.asyncio
async def test_clarification_planner():
    service = PlanningService()
    intent = MockIntentAnalysis(clarification_request=True)
    ctx = await service.create_plan(intent, {})
    
    assert ctx.plan.steps[0].required_capability == Capability.CLARIFICATION
