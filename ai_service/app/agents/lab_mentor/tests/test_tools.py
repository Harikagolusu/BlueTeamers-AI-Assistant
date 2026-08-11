import pytest
from app.agents.lab_mentor.tools.hint_generation import HintGenerationTool
from app.agents.lab_mentor.tools.hint_validation import HintValidationTool
from app.agents.lab_mentor.models import HintLevel
from app.tools.context import ToolContext

@pytest.mark.asyncio
async def test_hint_generation():
    tool = HintGenerationTool()
    res_l1 = await tool.execute(context=ToolContext(), blocker="Stuck on nmap", level=HintLevel.LEVEL_1)
    assert res_l1.level == HintLevel.LEVEL_1
    assert "concept" in res_l1.content.lower()

    res_l3 = await tool.execute(context=ToolContext(), blocker="Stuck on nmap", level=HintLevel.LEVEL_3)
    assert res_l3.level == HintLevel.LEVEL_3
    assert "tool" in res_l3.content.lower()

@pytest.mark.asyncio
async def test_hint_validation_safe():
    tool = HintValidationTool()
    res = await tool.execute(context=ToolContext(), hint_content="Try looking at the network traffic.")
    assert res["is_safe"] is True

@pytest.mark.asyncio
async def test_hint_validation_leakage():
    tool = HintValidationTool()
    res = await tool.execute(context=ToolContext(), hint_content="The answer is flag{12345}.")
    assert res["is_safe"] is False
    assert "Leakage" in res["feedback"]
