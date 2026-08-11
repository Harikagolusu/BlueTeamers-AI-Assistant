import pytest
from app.chat.intent.policies.ambiguity_policy import AmbiguityPolicy
from app.chat.intent.policies.fallback_policy import FallbackPolicy
from app.chat.intent.pipeline.context import IntentPipelineContext
from app.chat.intent.models.analysis_result import DetectedIntent
from app.chat.intent.models.intent_types import IntentType

@pytest.mark.asyncio
async def test_ambiguity_policy():
    policy = AmbiguityPolicy()
    
    # Test ambiguous pronoun without context
    ctx = IntentPipelineContext(query="what is it?")
    ctx.candidate_intents = [DetectedIntent(type=IntentType.GENERAL_CHAT, confidence=0.6, reason="")]
    
    ctx = await policy.apply(ctx)
    assert ctx.clarification_request is not None
    assert "Ambiguous" in ctx.clarification_request.reason
    
    # Test low confidence ambiguity
    ctx = IntentPipelineContext(query="random text")
    ctx.candidate_intents = [DetectedIntent(type=IntentType.UNKNOWN, confidence=0.1, reason="")]
    ctx = await policy.apply(ctx)
    assert ctx.clarification_request is not None
    assert "Low confidence" in ctx.clarification_request.reason

@pytest.mark.asyncio
async def test_fallback_policy():
    policy = FallbackPolicy()
    
    ctx = IntentPipelineContext(query="random")
    # Empty candidate intents triggers fallback
    ctx = await policy.apply(ctx)
    assert ctx.execution_recommendation is not None
    assert ctx.execution_recommendation.action == "FALLBACK_GENERAL"
