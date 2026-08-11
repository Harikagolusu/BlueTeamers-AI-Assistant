import pytest
from app.chat.intent.classifiers.rule_classifier import RuleIntentClassifier
from app.chat.intent.confidence.rule_evaluator import RuleConfidenceEvaluator
from app.chat.intent.models.entities import EntityCollection, ExtractedEntity
from app.chat.intent.models.intent_types import IntentType

@pytest.mark.asyncio
@pytest.mark.parametrize("query,expected", [
    # Platform intents must route to PLATFORM.
    ("What courses do I have?", IntentType.PLATFORM_COURSE),
    ("What courses am I enrolled in?", IntentType.PLATFORM_COURSE),
    ("Suggest SOC courses", IntentType.PLATFORM_COURSE),
    ("What is my progress?", IntentType.PLATFORM_PROGRESS),
    ("Show my certificates", IntentType.PLATFORM_CERTIFICATE),
    ("Which assessment should I take next?", IntentType.PLATFORM_ASSESSMENT),
    # Knowledge queries must route to RAG.
    ("Explain SIEM", IntentType.RAG_CHAT),
    ("SIEM vs SOC", IntentType.RAG_CHAT),
    ("How do firewalls work?", IntentType.RAG_CHAT),
    ("Explain MITRE ATT&CK", IntentType.MITRE_GUIDANCE),
    ("sigma rule example", IntentType.DETECTION_RULE),
    ("show me a detection rule", IntentType.DETECTION_RULE),
    ("T1059", IntentType.MITRE_GUIDANCE),
    # Off-topic content is refused (cybersecurity-only scope).
    ("Tell me a joke", IntentType.OFF_TOPIC),
    ("What is Python?", IntentType.OFF_TOPIC),
    ("How to cook pasta?", IntentType.OFF_TOPIC),
    ("What is the capital of France?", IntentType.OFF_TOPIC),
    # Cybersecurity-adjacent queries must stay in scope even if they
    # also contain off-topic words.
    ("python used for security automation", IntentType.RAG_CHAT),
    ("Hello", IntentType.GREETING),
    # Sprint 2 content-generation intents.
    ("Generate study notes on SIEM", IntentType.NOTES_GENERATION),
    ("Create revision notes for the phishing lesson", IntentType.NOTES_GENERATION),
    ("Make a cheat sheet for MITRE ATT&CK", IntentType.NOTES_GENERATION),
    ("Summarize the incident response process", IntentType.TOPIC_SUMMARY),
    ("Give me a quick revision of log analysis", IntentType.TOPIC_SUMMARY),
    ("TL;DR of this lesson", IntentType.TOPIC_SUMMARY),
    ("Explain CVE-2024-1234", IntentType.THREAT_INTEL),
    ("What is this malware family?", IntentType.THREAT_INTEL),
    ("Tell me about the APT28 threat actor", IntentType.THREAT_INTEL),
    # Sprint 3 SOC specialist intents (text-only mentoring assistants).
    ("Analyze this Wazuh alert", IntentType.WAZUH_LAB),
    ("What does the wazuh rule id 550 mean?", IntentType.WAZUH_LAB),
    ("Alert 1249 in wazuh", IntentType.WAZUH_LAB),
    ("Help me with the phishing email practice lab", IntentType.PRACTICE_LAB),
    ("How do I do the SIEM alert triage lab?", IntentType.PRACTICE_LAB),
    ("How do I investigate an alert?", IntentType.INVESTIGATION_GUIDANCE),
    ("Guide me through the investigation workflow", IntentType.INVESTIGATION_GUIDANCE),
    ("What does Windows event id 4625 mean?", IntentType.WINDOWS_EVENT_LOG),
    ("Explain the 4688 process creation event", IntentType.WINDOWS_EVENT_LOG),
    ("Analyze the logon events from the security log", IntentType.WINDOWS_EVENT_LOG),
    ("What is auth.log and how do I analyze it?", IntentType.LINUX_LOG),
    ("How do I read journalctl logs?", IntentType.LINUX_LOG),
    ("Analyze this IOC", IntentType.IOC_ANALYSIS),
    ("Is this domain malicious?", IntentType.IOC_ANALYSIS),
    ("Explain the MITRE ATT&CK tactic of privilege escalation", IntentType.MITRE_GUIDANCE),
    ("Write a Sigma rule for this", IntentType.DETECTION_RULE),
    ("Explain the structure of a YARA rule", IntentType.DETECTION_RULE),
])
async def test_routing_decisions(query, expected):
    classifier = RuleIntentClassifier()
    evaluator = RuleConfidenceEvaluator()

    entities = EntityCollection()
    if query == "T1059":
        entities = EntityCollection(entities=[ExtractedEntity(type="MITRE_TID", value="T1059")])
    elif query == "Is this domain malicious?":
        entities = EntityCollection(entities=[ExtractedEntity(type="DOMAIN", value="example.com")])

    intents = await classifier.classify(query, {}, entities)
    intents = await evaluator.evaluate(intents, query)

    assert intents[0].type == expected, f"{query!r}: got {intents[0].type.value}, expected {expected.value}"
