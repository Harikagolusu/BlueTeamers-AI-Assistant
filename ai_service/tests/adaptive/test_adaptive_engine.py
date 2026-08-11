"""Tests for the AdaptiveLearningEngine (Sprint 4 features 1-5)."""
import pytest

from app.adaptive.engine import AdaptiveLearningEngine
from app.adaptive.models import QuerySignals
from app.adaptive.store import SQLiteLearnerStore


@pytest.fixture
def engine(tmp_path):
    return AdaptiveLearningEngine(SQLiteLearnerStore(db_path=str(tmp_path / "adaptive.db")))


@pytest.mark.asyncio
async def test_default_depth_for_new_learner(engine):
    adaptation = await engine.adapt("u1", "Explain what a SIEM is", [])
    assert adaptation.base_level == "intermediate"
    assert adaptation.explanation_depth == 3
    assert adaptation.primary_topic is None


@pytest.mark.asyncio
async def test_topic_detection_sets_confidence(engine):
    adaptation = await engine.adapt("u1", "How do Wazuh decoders work?", [])
    assert adaptation.primary_topic == "wazuh"
    assert adaptation.confidence is None

    await engine.observe("u1", adaptation.topic_keys, adaptation.signals)
    adaptation2 = await engine.adapt("u1", "How do Wazuh decoders work?", [])
    assert adaptation2.confidence is not None
    assert 0.5 <= adaptation2.confidence <= 0.6
    assert "Wazuh" in adaptation2.adaptation_block


@pytest.mark.asyncio
async def test_expert_override_forces_max_depth(engine):
    adaptation = await engine.adapt("u1", "Give me the expert explanation of Sigma backends", [])
    assert adaptation.temporary_override == "expert"
    assert adaptation.explanation_depth == 5


@pytest.mark.asyncio
async def test_beginner_override_forces_simple_depth(engine):
    adaptation = await engine.adapt("u1", "Explain like I'm a beginner what an IOC is", [])
    assert adaptation.temporary_override == "beginner"
    assert adaptation.explanation_depth == 2


@pytest.mark.asyncio
async def test_confidence_moves_gradually(engine):
    a1 = await engine.adapt("u1", "How does Wazuh FIM work?", [])
    await engine.observe("u1", a1.topic_keys, a1.signals)
    profile = await engine.store.load_profile("u1")
    conf = profile.topic_confidences["wazuh"]
    assert conf.evidence_count == 1
    assert conf.confidence > 0.5
    assert conf.confidence < 0.6


@pytest.mark.asyncio
async def test_single_observation_never_jumps(engine):
    a1 = await engine.adapt("u1", "Expert deep dive into YARA rule optimization", [])
    for _ in range(1):
        await engine.observe("u1", a1.topic_keys, a1.signals)
    profile = await engine.store.load_profile("u1")
    conf = profile.topic_confidences["yara"].confidence
    assert 0.5 <= conf <= 0.6


@pytest.mark.asyncio
async def test_struggle_keeps_confidence_flat(engine):
    a1 = await engine.adapt("u1", "I don't understand how Sigma logsource works, it's confusing", [])
    await engine.observe("u1", a1.topic_keys, a1.signals)
    profile = await engine.store.load_profile("u1")
    conf = profile.topic_confidences["sigma"].confidence
    assert conf <= 0.5


@pytest.mark.asyncio
async def test_high_confidence_raises_depth(engine):
    profile = await engine.store.load_profile("u1")
    from app.adaptive.models import TopicConfidence
    import datetime
    profile.topic_confidences["mitre"] = TopicConfidence(
        topic_key="mitre", confidence=0.85, evidence_count=20,
        last_seen=datetime.datetime.now(datetime.timezone.utc),
    )
    await engine.store.save_profile(profile)
    adaptation = await engine.adapt("u1", "What are the MITRE sub-techniques?", [])
    assert adaptation.explanation_depth == 4  # 3 (intermediate) + 1


@pytest.mark.asyncio
async def test_base_level_derived_never_permanent(engine):
    a1 = await engine.adapt("u1", "Explain MITRE ATT&CK to me simply, I'm new", [])
    for _ in range(5):
        await engine.observe("u1", a1.topic_keys, a1.signals)
    profile = await engine.store.load_profile("u1")
    assert profile.base_level in ("beginner", "intermediate")


@pytest.mark.asyncio
async def test_signals_saved_in_adaptation(engine):
    adaptation = await engine.adapt("u1", "Can you give me a practical example of SIEM?", [])
    assert adaptation.signals.practical >= 1
    assert adaptation.signals.question >= 1


@pytest.mark.asyncio
async def test_adaptation_block_is_actionable(engine):
    adaptation = await engine.adapt("u1", "Explain MITRE ATT&CK T1059", [])
    block = adaptation.adaptation_block
    assert "Adaptive Learning" in block
    assert "MITRE ATT&CK" in block
    assert "Explanation depth" in block
