"""Cyber domain classification.

The Query Router must never generate responses or call the LLM. Classification is
a pure, deterministic function of the Intent Intelligence result plus a small
domain lexicon used only to split ambiguous intent buckets (e.g. a "course" query
may be a platform account question or a learning-coach request).
"""
import re
from enum import Enum
from typing import Optional

from app.chat.intent.models.analysis_result import IntentAnalysisResult
from app.chat.intent.models.intent_types import IntentType

# STEP 3A: Deterministic no-RAG for clearly conversational messages (zero LLM cost).
# Exact-match set - the entire meaningful message must be one of these, not
# containing additional knowledge content. Handles case, surrounding whitespace,
# and trailing punctuation (!?.). Internal content like "thanks, what is FIM?"
# does NOT match because the whole string is not in the set.
_CONVERSATIONAL_NO_RAG_EXACT = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good evening",
    "thank you",
    "thanks",
    "okay",
    "ok",
    "bye",
    "goodbye",
    "how are you",
    "how are you?",
    "nice",
    "great",
    "got it",
    "understood",
    "yes",
    "no",
}
# Normalized set without trailing ? for comparison (so "how are you?" and
# "how are you" both match after stripping punctuation).
_CONVERSATIONAL_NO_RAG_NORMALIZED = {
    re.sub(r"[!?.]+$", "", s).strip() for s in _CONVERSATIONAL_NO_RAG_EXACT
}


def is_conversational_no_rag(query: str) -> bool:
    """Return True if the query is a clearly non-knowledge conversational message.

    Zero LLM cost: pure Python string normalization, no embedding, no API.
    Only skips RAG when the *entire* meaningful message is an acknowledgement/
    greeting with no additional knowledge request. If uncertain, returns False
    so existing RAG flow is preserved.
    """
    if not query or not query.strip():
        return False
    q = query.strip().lower()
    # Collapse internal whitespace and strip trailing punctuation (!?.)
    q = re.sub(r"\s+", " ", q)
    q = re.sub(r"[!?.]+$", "", q).strip()
    # Also handle "how are you?" -> "how are you" after strip, so check normalized set
    return q in _CONVERSATIONAL_NO_RAG_NORMALIZED


class CyberDomain(str, Enum):
    GENERAL = "general"
    KNOWLEDGE = "knowledge"
    LEARNING = "learning"
    THREAT_INTEL = "threat_intel"
    INVESTIGATION = "investigation"
    PLATFORM = "platform"
    LAB = "lab"
    ASSESSMENT = "assessment"
    TOOLING = "tooling"
    # Sprint 3 - SOC Analyst Copilot specialist domains (one agent each).
    WAZUH_LAB = "wazuh_lab"
    PRACTICE_LAB = "practice_lab"
    INVESTIGATION_GUIDANCE = "investigation_guidance"
    WINDOWS_EVENT_LOG = "windows_event_log"
    LINUX_LOG = "linux_log"
    IOC_ANALYSIS = "ioc_analysis"
    MITRE_GUIDANCE = "mitre_guidance"
    DETECTION_RULE = "detection_rule"


_AMBIGUOUS_INTENTS = {
    IntentType.GENERAL_CHAT,
    IntentType.GREETING,
    IntentType.SMALL_TALK,
    IntentType.FOLLOW_UP,
    IntentType.UNKNOWN,
    IntentType.RAG_CHAT,
    IntentType.DOCUMENT_CHAT,
    IntentType.IMAGE_CHAT,
    IntentType.PLATFORM_COURSE,
    IntentType.PLATFORM_LAB,
}

_INTENT_TO_DOMAIN = {
    IntentType.GENERAL_CHAT: CyberDomain.GENERAL,
    IntentType.GREETING: CyberDomain.GENERAL,
    IntentType.SMALL_TALK: CyberDomain.GENERAL,
    IntentType.FOLLOW_UP: CyberDomain.GENERAL,
    IntentType.OFF_TOPIC: CyberDomain.GENERAL,
    IntentType.UNKNOWN: CyberDomain.GENERAL,
    IntentType.RAG_CHAT: CyberDomain.KNOWLEDGE,
    IntentType.DOCUMENT_CHAT: CyberDomain.KNOWLEDGE,
    IntentType.IMAGE_CHAT: CyberDomain.KNOWLEDGE,
    IntentType.TOOL_CHAT: CyberDomain.TOOLING,
    IntentType.SYSTEM_COMMAND: CyberDomain.TOOLING,
    IntentType.LAB_ASSISTANT: CyberDomain.LAB,
    IntentType.INVESTIGATION: CyberDomain.INVESTIGATION,
    IntentType.PLATFORM_COURSE: CyberDomain.PLATFORM,
    IntentType.PLATFORM_LAB: CyberDomain.LAB,
    IntentType.WAZUH_LAB: CyberDomain.WAZUH_LAB,
    IntentType.PRACTICE_LAB: CyberDomain.PRACTICE_LAB,
    IntentType.INVESTIGATION_GUIDANCE: CyberDomain.INVESTIGATION_GUIDANCE,
    IntentType.WINDOWS_EVENT_LOG: CyberDomain.WINDOWS_EVENT_LOG,
    IntentType.LINUX_LOG: CyberDomain.LINUX_LOG,
    IntentType.IOC_ANALYSIS: CyberDomain.IOC_ANALYSIS,
    IntentType.MITRE_GUIDANCE: CyberDomain.MITRE_GUIDANCE,
    IntentType.DETECTION_RULE: CyberDomain.DETECTION_RULE,
    IntentType.PLATFORM_PROGRESS: CyberDomain.PLATFORM,
    IntentType.PLATFORM_BADGE: CyberDomain.PLATFORM,
    IntentType.PLATFORM_CERTIFICATE: CyberDomain.PLATFORM,
    IntentType.PLATFORM_LEARNING_PATH: CyberDomain.PLATFORM,
    IntentType.PLATFORM_ASSESSMENT: CyberDomain.PLATFORM,
    IntentType.PLATFORM_DASHBOARD: CyberDomain.PLATFORM,
    IntentType.PLATFORM_PROFILE: CyberDomain.PLATFORM,
}

_LEARNING_SIGNALS = (
    "learning plan", "roadmap", "study plan", "career path", "path to",
    "how do i learn", "how should i learn", "what should i learn",
    "what should i study", "skill gap", "next course to take",
    "order should i take", "learn first", "build a plan", "journey",
)
_ASSESSMENT_SIGNALS = (
    "quiz", "assessment", "exam", "test me", "prepare for the", "certification",
    "practice questions", "readiness",
)
_INVESTIGATION_SIGNALS = (
    "investigat", "incident", "alert triage", "timeline", "triage", "case",
    "evidence", "ioc report", "forensic",
)
_THREAT_INTEL_SIGNALS = (
    "threat actor", "ttp", "mitre", "att&ck", "ioc", "malware family",
    "apt", "campaign", "indicator", "threat intelligence", "malicious ip",
)


class DomainClassifier:
    """Deterministic intent -> cyber domain classifier (no LLM, no response gen)."""

    def classify(
        self, query: str, intent_analysis: Optional[IntentAnalysisResult] = None
    ) -> tuple:
        """Return (CyberDomain, confidence, rationale)."""
        # STEP 3A: Early deterministic no-RAG for clearly conversational messages.
        # This is the final gate before agent selection: if the entire message is
        # just a greeting/acknowledgement, force GENERAL so no RAG engine is
        # selected. Zero LLM cost - pure string match. Knowledge queries like
        # "thanks, what is FIM?" do NOT match and proceed normally.
        if is_conversational_no_rag(query):
            return CyberDomain.GENERAL, 0.99, ["conversational-no-rag"]

        query_lower = (query or "").lower()
        primary_intent = None
        if intent_analysis and getattr(intent_analysis, "primary_intent", None):
            primary_intent = intent_analysis.primary_intent.type

        rationale = []

        # 1. Intent bucket is the primary signal.
        if primary_intent and primary_intent in _INTENT_TO_DOMAIN:
            domain = _INTENT_TO_DOMAIN[primary_intent]
            rationale.append(f"intent={primary_intent.value}")
        else:
            domain = CyberDomain.GENERAL
            rationale.append("intent=UNKNOWN")

        # 2. Domain lexicon may split an *ambiguous* intent bucket into a
        #    specialist agent. Specific intents (INVESTIGATION, LAB_ASSISTANT,
        #    TOOL_CHAT, PLATFORM_PROGRESS, ...) are never overridden.
        if primary_intent is None or primary_intent in _AMBIGUOUS_INTENTS:
            if any(sig in query_lower for sig in _LEARNING_SIGNALS):
                domain = CyberDomain.LEARNING
                rationale.append("learning-signal")
            elif any(sig in query_lower for sig in _INVESTIGATION_SIGNALS):
                domain = CyberDomain.INVESTIGATION
                rationale.append("investigation-signal")
            elif any(sig in query_lower for sig in _THREAT_INTEL_SIGNALS):
                domain = CyberDomain.THREAT_INTEL
                rationale.append("threat-intel-signal")
            elif any(sig in query_lower for sig in _ASSESSMENT_SIGNALS):
                domain = CyberDomain.ASSESSMENT
                rationale.append("assessment-signal")

        confidence = 0.95 if primary_intent in _INTENT_TO_DOMAIN else 0.5
        return domain, confidence, rationale
