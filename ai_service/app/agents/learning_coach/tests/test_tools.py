import pytest
from app.agents.learning_coach.tools.learning_analytics import LearningAnalyticsTool
from app.agents.learning_coach.tools.skill_gap_analysis import SkillGapAnalysisTool
from app.agents.learning_coach.tools.roadmap_generation import RoadmapGenerationTool
from app.agents.learning_coach.tools.recommendation_engine import RecommendationEngineTool
from app.agents.learning_coach.tools.progress_forecast import ProgressForecastTool
from app.agents.learning_coach.models import RecommendationPolicy
from app.tools.context import ToolContext

@pytest.mark.asyncio
async def test_learning_analytics_tool():
    tool = LearningAnalyticsTool()
    ctx = ToolContext(execution_id="1")
    res = await tool.execute(ctx, learner_id="test", history={})
    assert res.analytics.knowledge_growth == 12.0
    assert len(res.analytics.competency_trends) > 0
    assert res.roadmap_completion == 25.0

@pytest.mark.asyncio
async def test_skill_gap_analysis_tool():
    tool = SkillGapAnalysisTool()
    ctx = ToolContext(execution_id="1")
    res = await tool.execute(ctx, learner_id="test", history={})
    assert "Nmap Scanning" in res.weak_skills
    assert "Networking" in res.strong_skills

@pytest.mark.asyncio
async def test_recommendation_engine_tool():
    tool = RecommendationEngineTool()
    ctx = ToolContext(execution_id="1")
    policy = RecommendationPolicy()
    res = await tool.execute(ctx, skill_profile=None, policy=policy)
    assert len(res) > 0
    assert res[0].difficulty == "Beginner"
    assert res[0].expected_impact is not None
    assert res[0].explanation is not None
    assert res[0].explanation.recommendation_reason == "Direct alignment with Nmap Scanning gap"
