import pytest
from app.agents.knowledge_assistant.tools.concept_explanation import ConceptExplanationTool
from app.agents.knowledge_assistant.tools.concept_mapping import ConceptMappingTool
from app.agents.knowledge_assistant.tools.learning_path import LearningPathTool
from app.agents.knowledge_assistant.models import LearnerProfile, ExplanationLevel
from app.tools.context import ToolContext

@pytest.mark.asyncio
async def test_concept_explanation_beginner():
    tool = ConceptExplanationTool()
    profile = LearnerProfile(experience_level=ExplanationLevel.BEGINNER, preferred_explanation_depth="shallow")
    res = await tool.execute(context=ToolContext(), concept="Firewall", profile=profile, retrieved_context="")
    assert "Beginner" in res.summary
    assert "shallow" in res.detailed_explanation

@pytest.mark.asyncio
async def test_concept_explanation_expert():
    tool = ConceptExplanationTool()
    profile = LearnerProfile(experience_level=ExplanationLevel.EXPERT, preferred_explanation_depth="deep")
    res = await tool.execute(context=ToolContext(), concept="Zero Trust Architecture", profile=profile, retrieved_context="")
    assert "Expert" in res.summary
    assert "deep" in res.detailed_explanation

@pytest.mark.asyncio
async def test_learning_path_generation():
    tool = LearningPathTool()
    res = await tool.execute(context=ToolContext(), goal="Network Security", weak_topics=["DNS"], completed_topics=[])
    assert res.title == "Path towards: Network Security"
    assert len(res.steps) > 0
