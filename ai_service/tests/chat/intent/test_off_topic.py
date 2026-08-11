import pytest
from app.chat.intent.classifiers.rule_classifier import (
    RuleIntentClassifier,
    _has_cyber_relevance,
    _OFF_TOPIC_SIGNALS,
)
from app.chat.intent.confidence.rule_evaluator import RuleConfidenceEvaluator
from app.chat.intent.models.entities import EntityCollection
from app.chat.intent.models.intent_types import IntentType


@pytest.mark.asyncio
@pytest.mark.parametrize("query", [
    "Tell me a joke",
    "How do I cook pasta?",
    "What is the capital of France?",
    "Recommend a good movie",
    "What is Python?",
    "Tell me a cricket score",
])
async def test_clearly_off_topic_queries_are_refused(query):
    classifier = RuleIntentClassifier()
    evaluator = RuleConfidenceEvaluator()
    intents = await classifier.classify(query, {}, EntityCollection())
    intents = await evaluator.evaluate(intents, query)
    assert intents[0].type == IntentType.OFF_TOPIC, f"{query!r}: got {intents[0].type.value}"


@pytest.mark.asyncio
@pytest.mark.parametrize("query", [
    "python used for security automation",
    "How does a firewall work?",
    "Explain SIEM vs SOC",
    "how to write detection rules in python",
    "is python good for security?",
])
async def test_security_adjacent_queries_stay_in_scope(query):
    classifier = RuleIntentClassifier()
    intents = await classifier.classify(query, {}, EntityCollection())
    types = [i.type for i in intents]
    assert IntentType.OFF_TOPIC not in types, f"{query!r}: incorrectly refused"


def test_cyber_relevance_recognizes_security_terms():
    assert _has_cyber_relevance("how do i secure my python code")
    assert _has_cyber_relevance("python used for security automation")
    assert not _has_cyber_relevance("tell me a python joke")
    assert not _has_cyber_relevance("what is the capital of france")


def test_off_topic_signals_non_empty():
    assert len(_OFF_TOPIC_SIGNALS) >= 20
