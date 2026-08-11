import pytest
from app.agents.assessment_coach.tools.adaptive_question import AdaptiveQuestionTool
from app.agents.assessment_coach.tools.competency_evaluation import CompetencyEvaluationTool
from app.agents.assessment_coach.tools.readiness_assessment import ReadinessAssessmentTool
from app.agents.assessment_coach.models import QuestionDifficulty, AssessmentType

@pytest.mark.asyncio
async def test_adaptive_question_tool():
    tool = AdaptiveQuestionTool()
    res = await tool.execute(None, learner_id="test", current_difficulty="EXPERT")
    assert len(res) == 1
    assert res[0].difficulty == QuestionDifficulty.EXPERT
    assert res[0].type == AssessmentType.KNOWLEDGE

@pytest.mark.asyncio
async def test_competency_evaluation_tool():
    tool = CompetencyEvaluationTool()
    res = await tool.execute(None, learner_id="test", assessment_results=[])
    assert len(res) == 1
    assert res[0].score == 7.5

@pytest.mark.asyncio
async def test_readiness_assessment_tool():
    tool = ReadinessAssessmentTool()
    res = await tool.execute(None, learner_id="test", competency_profile={})
    assert len(res) == 2
    assert res[0].is_ready is False
