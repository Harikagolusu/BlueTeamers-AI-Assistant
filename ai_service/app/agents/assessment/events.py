from typing import List, Optional

from app.agents.events.agent_events import (
    AgentEvent,
    AssessmentAnsweredEvent,
    AssessmentCompletedEvent,
    AssessmentFailedEvent,
    AssessmentPassedEvent,
    AssessmentQuestionGeneratedEvent,
    AssessmentStartedEvent,
    LearningProgressUpdatedEvent,
    QuizSkippedEvent,
)


class AssessmentEventPublisher:
    """Publishes Assessment Agent lifecycle events onto the shared EventBus."""

    def __init__(self, event_bus, session_id_provider=None):
        self._bus = event_bus
        self._session_id_provider = session_id_provider

    def _session_id(self, session_key: str) -> str:
        if self._session_id_provider:
            return self._session_id_provider(session_key)
        return session_key or "assessment"

    def _publish(self, event: AgentEvent):
        if self._bus is not None:
            try:
                self._bus.publish(event)
            except Exception:
                pass

    def started(self, session_key: str, topic: str, difficulty: str):
        self._publish(AssessmentStartedEvent(
            session_id=self._session_id(session_key),
            topic=topic,
            difficulty=difficulty,
        ))

    def question_generated(self, session_key: str, question_id: str, question_type: str):
        self._publish(AssessmentQuestionGeneratedEvent(
            session_id=self._session_id(session_key),
            question_id=question_id,
            question_type=question_type,
        ))

    def answered(self, session_key: str, question_id: str, correct: bool, partial: bool):
        self._publish(AssessmentAnsweredEvent(
            session_id=self._session_id(session_key),
            question_id=question_id,
            correct=correct,
            partial=partial,
        ))

    def completed(self, session_key: str, score: int, total: int, passed: bool):
        self._publish(AssessmentCompletedEvent(
            session_id=self._session_id(session_key),
            score=score,
            total=total,
        ))
        event_cls = AssessmentPassedEvent if passed else AssessmentFailedEvent
        self._publish(event_cls(
            session_id=self._session_id(session_key),
            score=score,
            total=total,
        ))

    def learning_progress(self, session_key: str, topics: List[str], average_score: float):
        self._publish(LearningProgressUpdatedEvent(
            session_id=self._session_id(session_key),
            topics_completed=topics,
            average_score=average_score,
        ))

    def quiz_skipped(self, session_key: str, reason: str = ""):
        self._publish(QuizSkippedEvent(
            session_id=self._session_id(session_key),
            reason=reason,
        ))
