import logging
from typing import Optional

from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.agents.assessment.agent import AssessmentAgent
from app.agents.assessment.models import QuizSession, QuizSessionStatus

logger = logging.getLogger("app.chat.pipeline.assessment_stage")


def _with_suffix(generator, suffix: str):
    """Yields all tokens from an async generator, then the suffix text."""
    async def _wrapped():
        async for token in generator:
            yield token
        if suffix:
            yield suffix
    return _wrapped()


class AssessmentStage(IExecutionStage):
    """Runs the Assessment Agent as a post-answer overlay on the chat pipeline.

    Behaviors (never interrupts the user):
      - After a suitable learning answer, evaluates the learner's *course context*.
      - If the user is enrolled in a course matching the topic (and has not recently
        been assessed on it), appends a polite quiz offer.
      - On explicit confirmation, starts a turn-by-turn quiz inside the chat.
      - If the user is NOT enrolled in a matching course, NO quiz is offered;
        instead the stage delegates to the Course Recommendation service and appends
        available related courses (Enroll / View / skip).
      - Declines/cancels continue the conversation normally.
    """

    def __init__(self, agent: AssessmentAgent, settings=None, recommendation_service=None):
        self._agent = agent
        self._settings = settings
        self._recommendation_service = recommendation_service

    @property
    def name(self) -> str:
        return "Assessment"

    def _enabled(self) -> bool:
        if self._settings is None:
            return True
        return bool(getattr(self._settings, "ENABLE_ASSESSMENT_AGENT", True))

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if not self._enabled():
            return context

        # Never interrupt an active practice lab: the LabManager owns the turn
        # (including any completion offer). Assessment resumes via the normal
        # pipeline once the lab session is no longer active.
        if (context.metadata.get("lab") or {}).get("active"):
            return context

        result = context.metadata.get("execution_result")
        if not result:
            return context

        query = (context.metadata.get("query") or "").strip()
        if not query:
            return context

        selected_engine = context.metadata.get("selected_engine")
        if selected_engine in ("ASSESSMENT_COACH",):
            return context

        session_key = context.session_user or (context.metadata.get("user_id") or "").strip() or "anonymous"
        session = self._agent.get_session(session_key)

        # If there is an active/pending/completed quiz session, always route
        # through the AssessmentAgent regardless of the engine used.
        if session and session.status in (
            QuizSessionStatus.ACTIVE,
            QuizSessionStatus.PENDING_CONFIRM,
            QuizSessionStatus.COMPLETED,
            QuizSessionStatus.ABANDONED,
        ):
            pass  # fall through to _dispatch below
        elif selected_engine in ("PLATFORM",):
            return context

        try:
            new_result, meta = await self._dispatch(
                context=context,
                result=result,
                session=session,
                session_key=session_key,
                query=query,
            )
        except Exception as exc:
            logger.warning("AssessmentStage failed (%s); continuing normally", exc)
            return context

        if new_result is None:
            return context

        new_metadata = {**context.metadata, "execution_result": new_result}
        if meta:
            new_metadata["assessment"] = meta
        return context.model_copy(update={"metadata": new_metadata})

    async def _dispatch(self, context, result, session, session_key: str, query: str):
        if session and session.status == QuizSessionStatus.ACTIVE:
            return await self._handle_active(context, result, session, session_key, query)

        if session and session.status == QuizSessionStatus.PENDING_CONFIRM:
            return await self._handle_pending(context, result, session, session_key, query)

        if session and session.status == QuizSessionStatus.COMPLETED:
            return await self._handle_finished(context, result, session, session_key, query)

        if session and session.status == QuizSessionStatus.ABANDONED:
            await self._agent.clear_after(session_key)
            return await self._maybe_offer(context, result, session_key, query)

        return await self._maybe_offer(context, result, session_key, query)

    async def _handle_finished(self, context, result, session, session_key: str, query: str):
        if self._agent.is_another_quiz(query):
            message = await self._start_quiz(context, session_key, session.topic, query)
            if message:
                meta = {
                    "mode": "started",
                    "session": session_key,
                    "quiz": self._current_quiz_payload(session_key),
                }
                return self._takeover(result, message, meta), meta
            return None, None
        await self._agent.clear_after(session_key)
        return await self._maybe_offer(context, result, session_key, query)

    async def _handle_active(self, context, result, session, session_key: str, query: str):
        if self._agent.is_cancel(query):
            message = await self._agent.cancel(session_key)
            return self._takeover(result, message, {"mode": "cancelled", "session": session_key}), {
                "mode": "cancelled", "session": session_key
            }

        if self._agent.is_another_quiz(query):
            message = await self._start_quiz(context, session_key, session.topic, query)
            if message:
                return self._takeover(result, message, {
                    "mode": "started", "session": session_key,
                    "quiz": self._current_quiz_payload(session_key),
                }), {"mode": "started", "session": session_key}
            return None, None

        payload = await self._agent.answer(session_key, query)
        if not payload:
            return None, None

        if payload["kind"] == "summary":
            meta = {
                "mode": "summary",
                "session": session_key,
                "result": self._agent.result_payload(payload["result"]),
            }
        else:
            meta = {
                "mode": "next",
                "session": session_key,
                "quiz": self._current_quiz_payload(session_key),
            }

        return self._takeover(result, payload["message"], meta), meta

    def _current_quiz_payload(self, session_key: str):
        current = self._agent.get_session(session_key)
        return self._agent.quiz_payload(current) if current else None

    async def _handle_pending(self, context, result, session, session_key: str, query: str):
        if self._agent.is_confirmation(query):
            message = await self._start_quiz(context, session_key, session.topic, query)
            if not message:
                return None, None
            meta = {
                "mode": "started",
                "session": session_key,
                "quiz": self._current_quiz_payload(session_key),
            }
            return self._takeover(result, message, meta), meta

        if self._agent.is_decline(query):
            self._agent._events.quiz_skipped(session_key, "declined")
            await self._agent.clear_after(session_key)
            return None, {"mode": "skipped", "session": session_key}

        return None, {"mode": "pending", "session": session_key}

    async def _maybe_offer(self, context, result, session_key: str, query: str):
        intent_type = context.metadata.get("intent")
        routing = context.metadata.get("routing_decision")
        domain = context.metadata.get("domain")
        if not domain and routing is not None and hasattr(routing, "domain"):
            domain = routing.domain.value

        assessment = self._agent.evaluate_suitability(query, intent_type=intent_type, domain=domain)
        if not assessment.suitable:
            return None, {"mode": "off", "session": session_key}

        # Explicit quiz generation request ("Give me a 5-question quiz...") should
        # start immediately instead of just offering. The screenshot issue was that
        # "Give me a 5-question quiz on Network Security Monitoring" was routed to
        # PLATFORM (now fixed) but would have only offered, not generated the quiz.
        # Detect generation verbs and start directly.
        _explicit_quiz_lower = query.lower()
        _is_explicit_generation = any(
            p in _explicit_quiz_lower for p in (
                "give me a quiz", "give me quiz", "create a quiz", "create quiz",
                "generate a quiz", "generate quiz", "make a quiz", "make quiz",
                "5-question", "5 question", "multiple-choice quiz", "multiple choice quiz",
                "quiz me on", "test me on",
            )
        )
        if _is_explicit_generation:
            topic = assessment.topic or "cybersecurity"
            try:
                message = await self._start_quiz(context, session_key, topic, query)
                if message:
                    meta = {
                        "mode": "started",
                        "session": session_key,
                        "quiz": self._current_quiz_payload(session_key),
                        "topic": topic,
                    }
                    return self._takeover(result, message, meta), meta
            except Exception as exc:
                logger.warning("Assessment explicit start failed (%s); falling back to offer", exc)
            # fall through to offer if direct start fails

        pending = QuizSession(
            session_key=session_key,
            topic=assessment.topic or "cybersecurity",
            status=QuizSessionStatus.PENDING_CONFIRM,
        )
        self._agent._sessions.put(pending)

        offer = self._agent.offer_message()
        return self._append_offer(result, offer, {
            "mode": "offered", "session": session_key, "topic": pending.topic
        }), {"mode": "offered", "session": session_key}

    async def _recommend_course(self, context, result, decision, domain, token, session_key):
        """NOT enrolled -> delegate to the Course Recommendation service (no quiz)."""
        cards = []
        if self._recommendation_service is not None:
            try:
                recs = await self._recommendation_service.generate_for_domain(
                    token, domain=domain
                )
            except Exception as exc:
                logger.warning("Assessment course recommendation failed: %s", exc)
                recs = []
            cards = self._build_course_cards(recs)

        message = self._agent.course_recommendation_message()
        meta = {
            "mode": "course_recommended",
            "session": session_key,
            "topic": decision.topic or "",
            "cards": cards,
        }
        extra = {
            "platform_cards": cards,
            "platform": {"cards": cards, "actions": [], "context_used": ["course_recommendation"]},
            "recommendation_used": bool(cards),
        }
        return self._append_offer(result, message, meta, extra=extra), meta

    @staticmethod
    def _build_course_cards(recs) -> list:
        """Build platform course cards (Enroll / Go to course / Course info)."""
        cards = []
        for rec in recs:
            slug = rec.item_id
            cards.append({
                "title": rec.title,
                "type": "course",
                "difficulty": rec.difficulty,
                "duration": "N/A",
                "description": rec.reason or "",
                "progress": "",
                "action": {
                    "label": "Enroll course",
                    "action_type": "enroll_course",
                    "payload": {"id": slug, "url": f"/courses/{slug}/checkout"},
                },
                "actions": [
                    {
                        "label": "Enroll course",
                        "action_type": "enroll_course",
                        "payload": {"id": slug, "url": f"/courses/{slug}/checkout"},
                    },
                    {
                        "label": "Go to course",
                        "action_type": "open_course",
                        "payload": {"id": slug, "url": f"/courses/{slug}"},
                    },
                    {
                        "label": "Course info",
                        "action_type": "course_info",
                        "payload": {"id": slug},
                    },
                ],
            })
        return cards

    async def _start_quiz(self, context, session_key: str, topic: str, query: str) -> Optional[str]:
        conversation = ""
        if context.memory:
            conversation = str(context.memory.get("recent_context", ""))
        course_slug = None
        session = self._agent.get_session(session_key)
        if session and session.metadata:
            course_slug = session.metadata.get("course_slug")
        return await self._agent.start_quiz(
            session_key=session_key,
            topic=topic,
            conversation=conversation,
            user_key=session_key,
            course_slug=course_slug,
        )

    # ------------------------------------------------------------- result utils
    def _takeover(self, result, message: str, meta: dict):
        metadata = {k: v for k, v in result.metadata.items() if k != "generator"}
        metadata["assessment"] = meta
        return result.model_copy(update={"message": message, "metadata": metadata})

    def _append_offer(self, result, offer: str, meta: dict, extra: Optional[dict] = None):
        generator = result.metadata.get("generator")
        if generator is not None:
            metadata = {**result.metadata, "assessment": meta}
            if extra:
                metadata.update(extra)
            return result.model_copy(update={"metadata": metadata})

        message = (result.message or "") + offer
        metadata = {**result.metadata, "assessment": meta}
        if extra:
            metadata.update(extra)
        return result.model_copy(update={"message": message, "metadata": metadata})
