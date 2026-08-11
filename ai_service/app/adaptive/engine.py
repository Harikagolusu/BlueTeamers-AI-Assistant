"""AdaptiveLearningEngine: multi-signal learner model and per-request teaching plan.

Design rules (Sprint 4):
  - Confidence moves in small, gradual steps — a single interaction never
    swings the model and nothing permanently classifies the learner.
  - Temporary overrides (beginner / expert) shape only the current request.
  - The base level is derived, never stored as an identity.
"""
import datetime
from typing import List, Sequence

from app.adaptive.models import (
    LearnerAdaptation,
    LearnerProfile,
    QuerySignals,
    TopicConfidence,
)
from app.adaptive.signals import extract_signals
from app.adaptive.store import SQLiteLearnerStore
from app.adaptive.topics import detect_topics, topic_by_key

DEFAULT_BASE_LEVEL = "intermediate"

LEVEL_TO_DEPTH = {
    "beginner": 2,
    "intermediate": 3,
    "advanced": 4,
    "professional": 5,
}

_DEPTH_TERMINOLOGY = {
    1: "extremely simple",
    2: "simple",
    3: "balanced",
    4: "technical",
    5: "advanced",
}

_DEPTH_STYLE = {
    1: "analogy-first",
    2: "mentor-led",
    3: "balanced",
    4: "concise expert",
    5: "dense professional",
}

MIN_CONFIDENCE = 0.05
MAX_CONFIDENCE = 0.98

MAX_DELTA_PER_OBSERVATION = 0.08


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _score_to_level(score: float) -> str:
    if score < 0.4:
        return "beginner"
    if score < 0.6:
        return "intermediate"
    if score < 0.8:
        return "advanced"
    return "professional"


def derive_base_level(profile: LearnerProfile) -> str:
    """Derive a gradual base level from evidence-weighted topic confidence.

    Falls back to accumulated signals when no topic has evidence yet. The
    result never resets to a stored identity — it always reflects the trend.
    """
    confs = [c for c in profile.topic_confidences.values() if c.evidence_count > 0]
    if confs:
        weight = sum(c.evidence_count for c in confs)
        score = sum(c.confidence * c.evidence_count for c in confs) / weight
        return _score_to_level(score)

    counts = profile.signal_counts
    turns = max(counts.get("turns", 0), 1)
    net = (
        counts.get("expert_vocab", 0) * 2
        + counts.get("reinforce", 0)
        + counts.get("practical", 0)
        - counts.get("beginner_vocab", 0)
        - counts.get("struggle", 0) * 1.5
    )
    score = _clamp(0.5 + net / max(turns * 2, 1), 0.0, 1.0)
    return _score_to_level(score)


class AdaptiveLearningEngine:
    def __init__(self, store: SQLiteLearnerStore):
        self.store = store

    # ------------------------------------------------------------------ read
    async def adapt(
        self,
        user_id: str,
        query: str,
        recent_texts: Sequence[str] = (),
    ) -> LearnerAdaptation:
        profile = await self.store.load_profile(user_id)
        signals = extract_signals(query, recent_texts)

        texts = [query] + [t for t in list(recent_texts)[-2:] if t]
        topic_keys = detect_topics(texts)
        primary = topic_keys[0] if topic_keys else None
        primary_name = topic_by_key(primary).name if primary else None

        base_level = profile.base_level or DEFAULT_BASE_LEVEL
        depth = LEVEL_TO_DEPTH.get(base_level, 3)
        confidence = profile.confidence_for(primary)
        if primary and confidence is not None:
            if confidence < 0.4:
                depth -= 1
            elif confidence > 0.7:
                depth += 1

        if signals.beginner_override:
            depth = 2
        if signals.expert_override:
            depth = 5
        depth = int(_clamp(depth, 1, 5))

        temporary_override = None
        if signals.beginner_override:
            temporary_override = "beginner"
        elif signals.expert_override:
            temporary_override = "expert"

        adaptation = LearnerAdaptation(
            topic_keys=topic_keys,
            primary_topic=primary,
            primary_topic_name=primary_name,
            explanation_depth=depth,
            terminology=_DEPTH_TERMINOLOGY[depth],
            style=_DEPTH_STYLE[depth],
            confidence=round(confidence, 3) if confidence is not None else None,
            base_level=base_level,
            temporary_override=temporary_override,
            signals=signals,
        )
        adaptation.adaptation_block = self._build_block(adaptation)
        return adaptation

    # ------------------------------------------------------------------ write
    async def observe(
        self,
        user_id: str,
        topic_keys: List[str],
        signals: QuerySignals,
    ) -> LearnerProfile:
        """Gradually update the learner model from one observed turn."""
        profile = await self.store.load_profile(user_id)
        profile.signal_counts["turns"] = profile.signal_counts.get("turns", 0) + 1
        for attr in (
            "beginner_vocab", "expert_vocab", "practical",
            "struggle", "reinforce", "question",
        ):
            profile.signal_counts[attr] = profile.signal_counts.get(attr, 0) + getattr(signals, attr)

        delta = self._delta(signals)
        now = datetime.datetime.now(datetime.timezone.utc)
        for key in topic_keys:
            conf = profile.topic_confidences.get(key) or TopicConfidence(topic_key=key)
            conf.evidence_count += 1
            conf.last_seen = now
            conf.confidence = _clamp(conf.confidence + delta, MIN_CONFIDENCE, MAX_CONFIDENCE)
            profile.topic_confidences[key] = conf

        profile.base_level = derive_base_level(profile)
        profile.updated_at = now
        await self.store.save_profile(profile)
        return profile

    # ------------------------------------------------------------------ helpers
    def _delta(self, signals: QuerySignals) -> float:
        if signals.struggle:
            delta = -0.02 * min(signals.struggle, 3)
        elif signals.beginner_vocab and signals.question:
            delta = 0.01
        elif signals.reinforce or (signals.practical and signals.question):
            delta = 0.05
        elif signals.expert_vocab:
            delta = 0.06
        elif signals.question:
            delta = 0.02
        else:
            delta = 0.0

        if signals.expert_override:
            delta = max(delta, 0.03)
        if signals.beginner_override:
            delta = min(delta, 0.01)
        return _clamp(delta, -MAX_DELTA_PER_OBSERVATION, MAX_DELTA_PER_OBSERVATION)

    @staticmethod
    def _build_block(adaptation: LearnerAdaptation) -> str:
        lines = [
            "[Adaptive Learning]",
            f"The learner's base level is: {adaptation.base_level}.",
        ]
        if adaptation.primary_topic_name:
            conf = adaptation.confidence
            conf_txt = f" (estimated confidence {conf:.0%})" if conf is not None else ""
            lines.append(
                f"Current topic: {adaptation.primary_topic_name}{conf_txt}."
            )
        lines.append(
            f"Explanation depth for this answer: {adaptation.explanation_depth}/5 "
            f"(terminology: {adaptation.terminology}; style: {adaptation.style})."
        )
        if adaptation.temporary_override:
            lines.append(
                f"Temporary override: {adaptation.temporary_override}. "
                "Apply this override for THIS answer only; do not change the "
                "learner's base level."
            )
        lines.append(
            "Tailor vocabulary, example density, and structure to the depth "
            "above (deeper = fewer definitions, more precision; shallower = "
            "plain language, analogies, step-by-step)."
        )
        return "\n".join(lines)
