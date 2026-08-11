"""Tests for the AssessmentStage's offer path (simplified: no enrollment gate)."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.agents.assessment.models import SuitabilityAssessment, QuizSessionStatus
from app.chat.pipeline.assessment_stage import AssessmentStage
from app.models.chat.chat_models import ExecutionResult, ExecutionStatus


def make_result(message: str = "answer") -> ExecutionResult:
    return ExecutionResult(
        status=ExecutionStatus.SUCCESS,
        engine_name="RAG",
        message=message,
        metadata={},
    )


@pytest.mark.asyncio
async def test_stage_offers_quiz_when_suitable():
    agent = MagicMock()
    agent.evaluate_suitability = MagicMock(return_value=SuitabilityAssessment(
        suitable=True, topic="SIEM", confidence=0.8,
    ))
    agent.offer_message = MagicMock(return_value="\n\nWould you like a short quiz?")
    agent._sessions = MagicMock()
    stage = AssessmentStage(agent, settings=None)

    context = MagicMock(metadata={"domain": "knowledge", "token": "tok"})
    result = make_result()
    new_result, meta = await stage._maybe_offer(
        context=context, result=result, session_key="u", query="Explain SIEM"
    )
    assert meta["mode"] == "offered"
    assert "Would you like a short quiz?" in new_result.message
    pending = agent._sessions.put.call_args[0][0]
    assert pending.topic == "SIEM"
    assert pending.status == QuizSessionStatus.PENDING_CONFIRM


@pytest.mark.asyncio
async def test_stage_skips_when_not_suitable():
    agent = MagicMock()
    agent.evaluate_suitability = MagicMock(return_value=SuitabilityAssessment(
        suitable=False, reason="Not a learning context",
    ))
    stage = AssessmentStage(agent, settings=None)

    context = MagicMock(metadata={"domain": "general", "token": "tok"})
    result = make_result()
    new_result, meta = await stage._maybe_offer(
        context=context, result=result, session_key="u", query="hello"
    )
    assert meta["mode"] == "off"
    assert new_result is None
