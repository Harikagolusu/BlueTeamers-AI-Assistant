from typing import List
from app.chat.intent.interfaces import IConfidenceEvaluator
from app.chat.intent.models.analysis_result import DetectedIntent
from app.chat.intent.models.intent_types import IntentType


class RuleConfidenceEvaluator(IConfidenceEvaluator):
    """
    Deterministic confidence scoring for intent candidates.

    Priority (higher wins in the route planner):
      GREETING > PLATFORM_* > RAG_CHAT > TOOL_CHAT > GENERAL_CHAT
    """
    async def evaluate(self, intents: List[DetectedIntent], query: str) -> List[DetectedIntent]:
        evaluated = []
        for intent in intents:
            score = self._score(intent, query)
            intent.confidence = min(score, 0.99)
            evaluated.append(intent)

        # Sort by confidence descending for deterministic planner selection.
        evaluated.sort(key=lambda i: i.confidence, reverse=True)
        return evaluated

    @staticmethod
    def _score(intent: DetectedIntent, query: str) -> float:
        features = intent.matched_features or []

        if intent.type == IntentType.RAG_CHAT:
            score = 0.5
            if any(f.startswith("CVE") or f.startswith("T") for f in features):
                score += 0.4  # security entity → strong knowledge signal
            if any(f in _DOMAIN_FEATURES for f in features):
                score += 0.15
            if any(f in _CONTENT_REF_FEATURES for f in features):
                score += 0.1
            if any(f in _TRIGGER_FEATURES for f in features):
                score += 0.05
            return min(score, 0.9)

        if intent.type.value.startswith("PLATFORM_"):
            # Specific platform intents are authoritative whenever they fire.
            score = 0.85 + 0.04 * min(len(features), 3)
            return min(score, 0.97)

        if intent.type == IntentType.TOOL_CHAT:
            if any(a in features for a in ("scan", "lookup")):
                return 0.9
            return 0.6

        if intent.type == IntentType.THREAT_INTEL:
            # Threat-intel requests (CVE / IOC / malware family / actor /
            # technique) outrank the generic RAG bucket (max 0.9) so they route
            # to the dedicated Threat Intel engine.
            return 0.93

        if intent.type == IntentType.NOTES_GENERATION:
            return 0.9

        if intent.type == IntentType.TOPIC_SUMMARY:
            return 0.88

        if intent.type == IntentType.GREETING:
            return 0.99 if len(query.split()) < 5 else 0.6

        if intent.type == IntentType.LAB_ASSISTANT:
            # Lab-help requests are authoritative whenever they fire: outranks
            # RAG_CHAT (0.5-0.75) but stays below strong platform intents (>=0.85).
            return 0.88

        if intent.type in _SPRINT3_SCORES:
            # Sprint 3 specialist intents are authoritative for their domain:
            # they outrank the generic RAG bucket (max 0.9) and the threat-intel
            # bucket (0.93) where they overlap (IOC / MITRE questions).
            return _SPRINT3_SCORES[intent.type]

        if intent.type in (IntentType.INVESTIGATION,):
            return 0.75

        if intent.type == IntentType.GENERAL_CHAT:
            return 0.55

        if intent.type == IntentType.OFF_TOPIC:
            return 0.9

        # IMAGE_CHAT / DOCUMENT_CHAT / SMALL_TALK / FOLLOW_UP / UNKNOWN
        return 0.6


_DOMAIN_FEATURES = {
    "siem", "soc", "mitre", "att&ck", "ioc", "sigma", "event log",
    "event logs", "windows event", "firewall", "malware", "phishing",
    "command and control", "detection rule", "detection engineering",
    "threat hunting", "incident response", "log analysis", "packet capture",
    "tcp", "dns", "cve", "syn flood", "ddos", "payload", "exploit",
}
_CONTENT_REF_FEATURES = {
    "module", "lesson", "section", "chapter", "topic", "concept",
    "lecture", "lab", "course content", "learning path",
}
_SPRINT3_SCORES = {
    IntentType.WAZUH_LAB: 0.91,
    IntentType.PRACTICE_LAB: 0.91,
    IntentType.INVESTIGATION_GUIDANCE: 0.92,
    IntentType.WINDOWS_EVENT_LOG: 0.91,
    IntentType.LINUX_LOG: 0.91,
    IntentType.IOC_ANALYSIS: 0.95,
    IntentType.MITRE_GUIDANCE: 0.95,
    IntentType.DETECTION_RULE: 0.92,
}

_TRIGGER_FEATURES = {
    "what is", "what are", "what does", "how do", "how does", "how to",
    "explain", "define", "tell me about", "describe", "example", "examples",
    "difference between", "meaning of", "i don't understand", "i dont understand",
    "clarify", "walkthrough", "for beginners",
}
