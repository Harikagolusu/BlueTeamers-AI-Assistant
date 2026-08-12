from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.chat.pipeline.memory_stage import _memory_session_user
from app.memory.interfaces import IMemoryManager
from app.core.config import settings

import logging

logger = logging.getLogger("app.chat.pipeline.persistence")


class PersistenceStage(IExecutionStage):
    """Saves the conversation turns asynchronously.

    In addition to the short-term memory window (MemoryManager), this stage also
    records each turn to the ConversationService so that Recent Conversations,
    Favorites, search and resume work end-to-end.
    """

    def __init__(self, memory_manager: IMemoryManager, conversation_service=None):
        self._memory = memory_manager
        self._conversations = conversation_service

    @property
    def name(self) -> str:
        return "Persistence"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if not context.session_user:
            return context

        response = context.metadata.get("chat_response")
        if not response:
            # Fall back to the execution result if the composition stage hasn't
            # produced a chat_response yet.
            result = context.metadata.get("execution_result")
            if result and hasattr(result, "message"):
                response = result
            else:
                return context

        query = context.metadata.get("query") or ""
        ai_message = response.message or ""

        # Streaming engines return a "[Streaming Generator]" placeholder whose
        # real text only exists behind the SSE generator. Persisting it now
        # would pollute the conversation history and the short-term memory
        # window with fake content, so defer the whole turn to ChatService,
        # which persists the actual streamed text once the stream completes.
        result = context.metadata.get("execution_result")
        if (
            context.streaming_mode
            and result is not None
            and isinstance(getattr(result, "metadata", None), dict)
            and "generator" in result.metadata
            and ai_message == "[Streaming Generator]"
        ):
            result.metadata["_pending_turn"] = {
                "query": query,
                "session_user": context.session_user,
                "tenant_id": context.tenant_id or "default",
                "memory_session_user": _memory_session_user(context),
                "conversation_id": context.metadata.get("conversation_id"),
                "conversation_metadata": self._extract_conversation_metadata(context, response),
                "trace_id": str(context.trace_id),
            }
            return context

        turn_data = {
            "query": query,
            "response": ai_message,
            "citations": getattr(response, "metadata", {}).get("citations", []),
            "used_tools": getattr(response, "used_tools", []),
            "trace_id": str(context.trace_id),
        }

        await self._memory.save_turn(
            session_user=_memory_session_user(context),
            tenant_id=context.tenant_id or "default",
            turn_data=turn_data,
        )

        # Record the turn to the conversation store for Recent Conversations & Favorites.
        if self._conversations is not None and getattr(settings, "CONVERSATION_PERSISTENCE_ENABLED", True):
            try:
                conv_meta = self._extract_conversation_metadata(context, response)
                conversation_id = context.metadata.get("conversation_id")
                await self._conversations.record_turn(
                    user_id=context.session_user,
                    conversation_id=conversation_id,
                    user_message=query,
                    ai_message=ai_message,
                    metadata=conv_meta,
                )
            except Exception as exc:
                logger.warning("Failed to record conversation turn: %s", exc)

        return context

    @staticmethod
    def _extract_conversation_metadata(context, response) -> dict:
        """Derive conversation_type, course, and assessment metadata from the result."""
        meta = {}
        result = context.metadata.get("execution_result")
        result_meta = getattr(result, "metadata", {}) or {}
        response_meta = getattr(response, "metadata", {}) or {}        # Conversation type from engine / domain / assessment mode.
        engine = result_meta.get("engine") or response_meta.get("engine") or ""
        domain = result_meta.get("domain") or response_meta.get("domain") or ""
        assessment = result_meta.get("assessment") or response_meta.get("assessment") or {}

        if isinstance(assessment, dict) and assessment.get("mode") in ("started", "next", "summary"):
            meta["conversation_type"] = "assessment"
            if assessment.get("course_slug"):
                meta["course_id"] = assessment["course_slug"]
        elif engine in ("RAG", "MITRE_GUIDANCE", "DETECTION_RULE") or domain == "knowledge":
            meta["conversation_type"] = "learning"
        elif engine in ("INVESTIGATION", "INVESTIGATION_GUIDANCE",
                        "WINDOWS_EVENT_LOG", "LINUX_LOG", "IOC_ANALYSIS"):
            meta["conversation_type"] = "investigation"
        elif engine in ("TOOL",):
            meta["conversation_type"] = "tool"
        elif engine in ("LAB_MENTOR", "WAZUH_LAB", "PRACTICE_LAB") or domain == "lab":
            meta["conversation_type"] = "lab"
        elif engine in ("PLATFORM",):
            meta["conversation_type"] = "chat"
        else:
            meta["conversation_type"] = "chat"

        # Course info from platform cards or assessment metadata.
        platform = result_meta.get("platform") or response_meta.get("platform") or {}
        if isinstance(platform, dict) and platform.get("cards"):
            cards = platform["cards"]
            if cards and isinstance(cards, list):
                first = cards[0] if isinstance(cards[0], dict) else {}
                if first.get("type") == "course" and first.get("title"):
                    meta["course_title"] = first["title"]

        # Assessment score from a completed quiz summary.
        if isinstance(assessment, dict) and assessment.get("mode") == "summary":
            result_payload = assessment.get("result") or {}
            if isinstance(result_payload, dict):
                score = result_payload.get("score")
                total = result_payload.get("total")
                if score is not None and total is not None:
                    meta["assessment_score"] = f"{score}/{total}"

        return meta

