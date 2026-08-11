import pytest
from app.services.lab.models import LabState, HintValidationPolicy, MistakeCategory, LabSession
from app.services.lab.state_machine import LabStateMachine
from app.services.lab.exceptions import InvalidStateTransitionError, TerminalStateError
from app.agents.lab_mentor.tools.hint_validation import HintValidationTool
from app.agents.lab_mentor.tools.mistake_detection import MistakeDetectionTool
from app.tools.context import ToolContext

def test_valid_transitions():
    sm = LabStateMachine()
    assert sm.current_state == LabState.NOT_STARTED
    sm.transition(LabState.INITIALIZING)
    assert sm.current_state == LabState.INITIALIZING
    sm.transition(LabState.IN_PROGRESS)
    assert sm.current_state == LabState.IN_PROGRESS

def test_invalid_transitions():
    sm = LabStateMachine()
    with pytest.raises(InvalidStateTransitionError):
        sm.transition(LabState.IN_PROGRESS) # From NOT_STARTED

def test_terminal_protection():
    sm = LabStateMachine()
    sm.current_state = LabState.COMPLETED
    with pytest.raises(TerminalStateError):
        sm.transition(LabState.NOT_STARTED)

@pytest.mark.asyncio
async def test_hint_validation_policy():
    tool = HintValidationTool()
    policy = HintValidationPolicy(
        check_flags=True,
        check_passwords=True,
        check_tokens=True
    )
    
    ctx = ToolContext(execution_id="1")
    # Test flag
    res = await tool.execute(ctx, hint_content="try flag{test}", policy=policy)
    assert not res["is_safe"]
    
    # Test password
    res = await tool.execute(ctx, hint_content="admin:password123", policy=policy)
    assert not res["is_safe"]
    
    # Test token
    res = await tool.execute(ctx, hint_content="token eyjhbGciOi", policy=policy)
    assert not res["is_safe"]
    
    # Test safe
    res = await tool.execute(ctx, hint_content="look at the headers", policy=policy)
    assert res["is_safe"]

@pytest.mark.asyncio
async def test_mistake_categorization():
    tool = MistakeDetectionTool()
    ctx = ToolContext(execution_id="1")
    
    res = await tool.execute(ctx, action="stuck")
    assert res["category"] == MistakeCategory.CONCEPT
    
    res = await tool.execute(ctx, action="syntax error")
    assert res["category"] == MistakeCategory.SYNTAX
    
    res = await tool.execute(ctx, action="submit flag")
    assert res["category"] == MistakeCategory.WORKFLOW
