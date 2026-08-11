"""Data models for the adaptive learning intelligence subsystem."""
import datetime
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional


def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


@dataclass
class TopicConfidence:
    """Smoothed, per-topic estimate of learner understanding.

    Confidence moves toward 1.0 on engagement and drifts back very slowly; it
    is never a hard classification and never reaches absolute bounds.
    """
    topic_key: str
    confidence: float = 0.5
    evidence_count: int = 0
    last_seen: datetime.datetime = field(default_factory=_now)

    def to_dict(self) -> dict:
        return {
            "topic_key": self.topic_key,
            "confidence": round(self.confidence, 3),
            "evidence_count": self.evidence_count,
            "last_seen": self.last_seen.isoformat(),
        }


@dataclass
class LearnerProfile:
    """Persisted state for a single learner: base level + topic confidences.

    The base level is derived from accumulated signals and is recomputed
    gradually; nothing here permanently classifies the learner.
    """
    user_id: str
    base_level: str = "intermediate"
    topic_confidences: Dict[str, TopicConfidence] = field(default_factory=dict)
    signal_counts: Dict[str, int] = field(default_factory=dict)
    updated_at: datetime.datetime = field(default_factory=_now)

    def confidence_for(self, topic_key: Optional[str]) -> Optional[float]:
        if not topic_key:
            return None
        conf = self.topic_confidences.get(topic_key)
        return conf.confidence if conf else None


@dataclass
class QuerySignals:
    """Boolean/statistical markers extracted from the current request."""
    beginner_override: bool = False
    expert_override: bool = False
    beginner_vocab: int = 0
    expert_vocab: int = 0
    practical: int = 0
    struggle: int = 0
    reinforce: int = 0
    question: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LearnerAdaptation:
    """The per-request teaching plan derived from the learner model."""
    topic_keys: List[str] = field(default_factory=list)
    primary_topic: Optional[str] = None
    primary_topic_name: Optional[str] = None
    explanation_depth: int = 3
    terminology: str = "balanced"
    style: str = "balanced"
    confidence: Optional[float] = None
    base_level: str = "intermediate"
    temporary_override: Optional[str] = None
    signals: QuerySignals = field(default_factory=QuerySignals)
    adaptation_block: str = ""

    def to_dict(self) -> dict:
        return {
            "topic_keys": self.topic_keys,
            "primary_topic": self.primary_topic,
            "primary_topic_name": self.primary_topic_name,
            "explanation_depth": self.explanation_depth,
            "terminology": self.terminology,
            "style": self.style,
            "confidence": self.confidence,
            "base_level": self.base_level,
            "temporary_override": self.temporary_override,
            "signals": self.signals.to_dict(),
            "adaptation_block": self.adaptation_block,
        }


@dataclass
class SessionMemoryState:
    """Conversation-scoped memory: rolling turns + compacted summary + facts.

    Independent per (user, conversation): context isolation. Tracks an optional
    active investigation and any files uploaded during the conversation.
    """
    user_id: str
    conversation_id: Optional[str]
    rolling_messages: List[dict] = field(default_factory=list)
    summary: str = ""
    facts: List[str] = field(default_factory=list)
    investigation: dict = field(default_factory=dict)
    uploaded_files: List[dict] = field(default_factory=list)
    updated_at: datetime.datetime = field(default_factory=_now)

    def to_dict(self) -> dict:
        return {
            "conversation_id": self.conversation_id,
            "rolling_messages": self.rolling_messages,
            "summary": self.summary,
            "facts": self.facts,
            "investigation": self.investigation,
            "uploaded_files": self.uploaded_files,
            "updated_at": self.updated_at.isoformat(),
        }
