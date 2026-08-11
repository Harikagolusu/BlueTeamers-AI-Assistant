import pytest
from app.chat.intent.classifiers.rule_classifier import RuleIntentClassifier
from app.chat.intent.confidence.rule_evaluator import RuleConfidenceEvaluator
from app.chat.intent.models.entities import EntityCollection, ExtractedEntity
from app.chat.intent.models.intent_types import IntentType

@pytest.mark.asyncio
async def test_rule_classifier_and_confidence():
    classifier = RuleIntentClassifier()
    evaluator = RuleConfidenceEvaluator()
    
    # 1. RAG query with entities: a CVE entity now routes to the dedicated
    # Threat Intel intent (0.93 > RAG max 0.9), per the Sprint 2 feature.
    entities = EntityCollection(entities=[ExtractedEntity(type="CVE", value="CVE-2024-1234")])
    query = "explain how this works"
    
    intents = await classifier.classify(query, {}, entities)
    assert intents[0].type == IntentType.THREAT_INTEL
    
    intents = await evaluator.evaluate(intents, query)
    assert intents[0].confidence >= 0.9 # Threat intel confidence floor
    
    # 2. Greeting
    intents = await classifier.classify("Hello there", {}, EntityCollection())
    intents = await evaluator.evaluate(intents, "Hello there")
    assert intents[0].type == IntentType.GREETING
    assert intents[0].confidence == 0.99
    
    # 3. Tool request
    intents = await classifier.classify("scan 192.168.1.1", {}, EntityCollection())
    intents = await evaluator.evaluate(intents, "scan 192.168.1.1")
    assert intents[0].type == IntentType.TOOL_CHAT
    assert intents[0].confidence >= 0.9

    # 4. Platform info
    intents = await classifier.classify("suggest a course for SOC", {}, EntityCollection())
    intents = await evaluator.evaluate(intents, "suggest a course for SOC")
    assert intents[0].type == IntentType.PLATFORM_COURSE
    assert intents[0].confidence >= 0.9
