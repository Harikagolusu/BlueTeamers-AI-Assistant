"""Adaptive learning pipeline stages.

AdaptiveContextStage (load): computes the per-request teaching plan and the
conversation's session memory, then injects both into context.memory where
SimplePromptBuilder picks them up. Runs after MemoryLoadStage.

AdaptivePersistenceStage (store): after the response is produced, gradually
updates the learner model and persists the session memory (rolling context,
summary, facts, investigation, files).
"""
from app.chat.context.execution_context import ExecutionContext
from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.adaptive.models import LearnerAdaptation, QuerySignals
from app.adaptive.service import AdaptiveLearningService


def _recent_texts(context: ExecutionContext) -> list:
    memory = context.memory or {}
    return [m.get("content", "") for m in memory.get("messages", [])]


def _response_message(context: ExecutionContext) -> str:
    response = context.metadata.get("chat_response")
    if response is not None and getattr(response, "message", None):
        return response.message
    result = context.metadata.get("execution_result")
    if result is not None and getattr(result, "message", None):
        return result.message
    return ""


def _engine_name(context: ExecutionContext) -> str:
    result = context.metadata.get("execution_result")
    if result is not None and getattr(result, "engine_name", None):
        return result.engine_name
    response = context.metadata.get("chat_response")
    if response is not None:
        return (getattr(response, "metadata", {}) or {}).get("engine", "")
    return ""


def _rebuild_adaptation(data: dict) -> LearnerAdaptation:
    """Rehydrate a stored adaptation (dict) for persistence bookkeeping."""
    signals = data.get("signals") or {}
    return LearnerAdaptation(
        topic_keys=data.get("topic_keys", []),
        primary_topic=data.get("primary_topic"),
        primary_topic_name=data.get("primary_topic_name"),
        explanation_depth=data.get("explanation_depth", 3),
        terminology=data.get("terminology", "balanced"),
        style=data.get("style", "balanced"),
        confidence=data.get("confidence"),
        base_level=data.get("base_level", "intermediate"),
        temporary_override=data.get("temporary_override"),
        signals=QuerySignals(**signals),
    )


class AdaptiveContextStage(IExecutionStage):
    """Loads the learner model + session memory and injects them into the prompt."""

    def __init__(self, service: AdaptiveLearningService):
        self._service = service

    @property
    def name(self) -> str:
        return "AdaptiveLearning"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if not context.session_user:
            return context

        query = context.metadata.get("query") or ""
        conversation_id = context.metadata.get("conversation_id")
        adaptation = await self._service.adapt(
            context.session_user,
            query,
            _recent_texts(context),
        )
        session = await self._service.load_session(context.session_user, conversation_id)

        memory = {
            **context.memory,
            "adaptive_learning": adaptation.to_dict(),
            "session_memory": session.to_dict(),
        }
        return context.with_memory(memory)


class AdaptivePersistenceStage(IExecutionStage):
    """Gradually updates the learner model and persists session memory."""

    def __init__(self, service: AdaptiveLearningService):
        self._service = service

    @property
    def name(self) -> str:
        return "AdaptivePersistence"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if not context.session_user:
            return context

        query = context.metadata.get("query") or ""
        ai_message = _response_message(context)
        adaptation_data = (context.memory or {}).get("adaptive_learning") or {}
        if not adaptation_data:
            return context

        try:
            await self._service.observe_turn(
                context.session_user,
                context.metadata.get("conversation_id"),
                query,
                ai_message,
                _rebuild_adaptation(adaptation_data),
                engine=_engine_name(context),
                files=context.metadata.get("files"),
                images=context.metadata.get("images"),
            )
        except Exception:
            # Adaptive learning must never break the chat flow.
            pass
        return context
