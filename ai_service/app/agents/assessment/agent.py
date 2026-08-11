import logging
import re
from datetime import datetime
from typing import Dict, List, Optional

from app.agents.assessment import fallback as fallback_lib
from app.agents.assessment import prompts as prompt_lib
from app.agents.assessment.course_context import (
    CourseContextService,
    CourseOffer,
    CourseOfferAction,
)
from app.agents.assessment.events import AssessmentEventPublisher
from app.agents.assessment.models import (
    AnswerRecord,
    DifficultyLevel,
    QuestionType,
    QuizQuestion,
    QuizResult,
    QuizSession,
    QuizSessionStatus,
    SuitabilityAssessment,
)
from app.agents.assessment.session_store import InMemoryQuizSessionStore
from app.agents.assessment.profile_store import InMemoryAssessmentProfileStore
from app.llm.interfaces import ILLMService
from app.platform.models import Course

logger = logging.getLogger("app.agents.assessment.agent")

_LEARNING_SIGNALS = [
    "explain", "explain how", "teach me", "what is", "what are", "what's",
    "how does", "how do", "how to", "learn", "learning", "study", "understand",
    "concept", "certification", "interview prep", "prepare", "practice",
    "recap", "quiz me", "test me", "help me learn", "breakdown",
]

_BLOCK_SIGNALS = [
    "bug", "debug", "fix this", "compile", "syntax error", "traceback",
    "write code", "generate", "draw", "image", "meme", "thank", "thanks",
    "greeting", "hello there", "just saying hi",
]

_SUITABLE_INTENTS = {
    "RAG_CHAT", "GENERAL_CHAT", "PLATFORM_LEARNING_PATH", "DOCUMENT_CHAT",
}

_SUITABLE_DOMAINS = {"knowledge", "learning", "assessment"}

_EXPLICIT_ASSESSMENT_SIGNALS = [
    "quiz me", "test me", "give me a quiz", "practice", "test my knowledge",
    "assess me", "challenge me", "mock exam", "certification prep",
]

_CONFIRMATION_PHRASES = [
    "yes", "yeah", "yep", "sure", "ok", "okay", "alright", "absolutely",
    "definitely", "let's", "lets", "let's do it", "lets do it", "let's start",
    "lets start", "start", "go ahead", "go", "sounds good", "bring it on",
    "i'm ready", "im ready", "yes please", "sure thing",
]

_DECLINE_PHRASES = [
    "no", "no thanks", "not now", "later", "skip", "pass", "next time",
    "maybe later", "no thank you", "i'm good", "im good", "not right now",
    "not now", "thanks but no",
]

_CANCEL_PHRASES = [
    "stop", "cancel", "quit", "abort", "end quiz", "stop the quiz",
    "i'm done", "im done", "enough", "never mind",
]

_ANOTHER_QUIZ_PHRASES = [
    "another quiz", "another one", "one more", "again", "retake", "new quiz",
    "quiz again", "another round",
]

_ALL_QUESTION_TYPES = [
    "mcq", "true_false", "fill_in_blank", "short_answer",
    "scenario", "interview", "code",
]

_DIFFICULTY_ALIASES = {
    "easy": DifficultyLevel.BEGINNER,
    "beginner": DifficultyLevel.BEGINNER,
    "intermediate": DifficultyLevel.INTERMEDIATE,
    "medium": DifficultyLevel.INTERMEDIATE,
    "advanced": DifficultyLevel.ADVANCED,
    "hard": DifficultyLevel.ADVANCED,
    "expert": DifficultyLevel.ADVANCED,
    "interview": DifficultyLevel.INTERVIEW,
    "real-world": DifficultyLevel.REAL_WORLD,
    "real world": DifficultyLevel.REAL_WORLD,
}

_PASS_THRESHOLD = 0.6


def _normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


class AssessmentAgent:
    """Interactive learning & quiz agent.

    Runs entirely inside the chat: offers a quiz after a suitable learning answer,
    waits for explicit confirmation, then asks questions turn-by-turn, grades each
    answer with constructive feedback, and finishes with a scored summary. Reuses
    the shared EventBus, memory (profile store) and the ILLMService for generation.
    """

    def __init__(
        self,
        llm: ILLMService,
        session_store: Optional[InMemoryQuizSessionStore] = None,
        profile_store: Optional[InMemoryAssessmentProfileStore] = None,
        event_publisher: Optional[AssessmentEventPublisher] = None,
        obs=None,
        settings=None,
        course_context: Optional[CourseContextService] = None,
    ):
        self._llm = llm
        self._sessions = session_store or InMemoryQuizSessionStore()
        self._profiles = profile_store or InMemoryAssessmentProfileStore()
        self._events = event_publisher or AssessmentEventPublisher(None)
        self._obs = obs
        self._settings = settings
        self._course_context = course_context

    # ------------------------------------------------------------------ config
    def quiz_payload(self, session: QuizSession) -> dict:
        """Structured question payload for the frontend quiz card."""
        question = session.current_question
        return {
            "index": session.current_index + 1 if question else session.length,
            "total": session.length,
            "question_id": question.question_id if question else None,
            "text": question.text if question else "",
            "options": list(question.options) if question else [],
            "type": question.type.value if question else "",
            "difficulty": question.difficulty.value if question else session.difficulty.value,
            "topic": question.topic if question and question.topic else session.topic,
        }

    @staticmethod
    def result_payload(result: QuizResult) -> dict:
        """Structured result payload for the frontend summary card."""
        return {
            "score": result.score,
            "total": result.total,
            "passed": result.passed,
            "strengths": list(result.strengths),
            "weak_areas": list(result.weak_areas),
            "recommendations": list(result.recommendations),
            "next_topic": result.next_topic,
            "difficulty_reached": result.difficulty_reached.value,
        }

    def _cfg(self) -> dict:
        s = self._settings
        if s is None:
            return {}
        return {
            "enabled": bool(getattr(s, "ENABLE_ASSESSMENT_AGENT", True)),
            "min_confidence": float(getattr(s, "ASSESSMENT_MINIMUM_CONFIDENCE_THRESHOLD", 0.6)),
            "default_length": int(getattr(s, "ASSESSMENT_DEFAULT_QUIZ_LENGTH", 5)),
            "default_difficulty": str(getattr(s, "ASSESSMENT_DEFAULT_DIFFICULTY", "beginner")),
            "max_questions": int(getattr(s, "ASSESSMENT_MAXIMUM_QUESTIONS", 10)),
            "adaptive": bool(getattr(s, "ASSESSMENT_ALLOW_ADAPTIVE_DIFFICULTY", True)),
            "require_enrollment": bool(getattr(s, "ASSESSMENT_REQUIRE_ENROLLMENT", True)),
            "recent_window_seconds": int(getattr(s, "ASSESSMENT_RECENT_WINDOW_SECONDS", 0)),
            "recommendation_count": int(getattr(s, "ASSESSMENT_COURSE_RECOMMENDATION_COUNT", 3)),
        }

    # --------------------------------------------------------------- suitability
    def evaluate_suitability(
        self,
        query: str,
        intent_type: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> SuitabilityAssessment:
        cfg = self._cfg()
        if not cfg.get("enabled", True):
            return SuitabilityAssessment(suitable=False, reason="Assessment agent disabled")

        text = query.lower()
        norm = _normalise(query)
        signals: List[str] = []

        if intent_type in {"GREETING", "SMALL_TALK", "SYSTEM_COMMAND", "IMAGE_CHAT",
                           "INVESTIGATION", "LAB_ASSISTANT", "TOOL_CHAT"}:
            return SuitabilityAssessment(
                suitable=False, reason=f"Intent {intent_type} is not a learning context"
            )
        if intent_type and intent_type.startswith("PLATFORM_") and intent_type != "PLATFORM_LEARNING_PATH":
            return SuitabilityAssessment(
                suitable=False, reason="Platform lookup is not a learning context"
            )

        for signal in _BLOCK_SIGNALS:
            if signal in norm:
                return SuitabilityAssessment(
                    suitable=False, reason=f"Blocked signal '{signal}'", signals=[signal]
                )

        confidence = 0.35
        if intent_type in _SUITABLE_INTENTS:
            confidence += 0.2
            signals.append(f"intent:{intent_type}")
        if domain and domain.lower() in _SUITABLE_DOMAINS:
            confidence += 0.15
            signals.append(f"domain:{domain}")

        for signal in _LEARNING_SIGNALS:
            if signal in text:
                confidence += 0.15
                signals.append(f"learn:{signal}")

        for signal in _EXPLICIT_ASSESSMENT_SIGNALS:
            if signal in text:
                confidence = 0.95
                signals.append(f"assess:{signal}")
                break

        confidence = round(min(confidence, 0.97), 2)
        suitable = confidence >= cfg.get("min_confidence", 0.6)
        return SuitabilityAssessment(
            suitable=suitable,
            confidence=confidence,
            reason="Learning/assessment request detected" if suitable else "Not a learning context",
            signals=signals,
            topic=self._extract_topic(query),
        )

    def _extract_topic(self, query: str) -> str:
        text = query.strip()
        if not text:
            return "cybersecurity"
        text = re.sub(
            r"^(explain|explain how|teach me|what is|what are|what's|how does|how do|"
            r"how to|learn about|learn|study|understand|tell me about|about|quiz me on|"
            r"test me on|practice)\b\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )
        text = text.strip(" .?!:")
        return text[:80] or "cybersecurity"

    def parse_difficulty(self, text: str) -> Optional[DifficultyLevel]:
        norm = _normalise(text)
        for alias, level in _DIFFICULTY_ALIASES.items():
            if _normalise(alias) in norm:
                return level
        return None

    # ------------------------------------------------------------ offer / intents
    @staticmethod
    def offer_message(course_title: Optional[str] = None) -> str:
        """Polite quiz offer shown after a suitable learning answer.

        When a specific enrolled course matches, the offer is course-aware.
        """
        if course_title:
            return (
                "\n\nWould you like to check your understanding of **"
                + course_title
                + "** with a short quiz? I can help assess your grasp of this "
                "topic with a few questions. Just say yes to begin."
            )
        return (
            "\n\nWould you like to test your understanding with a short quiz? "
            "I can help you practice this concept with a few questions. Just say yes to begin."
        )

    @staticmethod
    def course_recommendation_message() -> str:
        """Message shown when the user is NOT enrolled (no quiz is offered)."""
        return (
            "\n\nI won't quiz you on this just yet — since you're not currently "
            "enrolled in a course covering this topic, I'd suggest learning it in "
            "a structured way first. If you'd like, here are some courses you can "
            "explore (you can also say \"maybe later\" to skip them)."
        )

    async def queue_offer(self, session_key: str, topic: str) -> str:
        """Queue a pending-confirmation quiz offer (used by the lab completion).

        Mirrors AssessmentStage._maybe_offer: records a PENDING_CONFIRM session so
        that a subsequent "yes" starts the quiz through the normal pipeline.
        """
        pending = QuizSession(
            session_key=session_key,
            topic=topic or "cybersecurity",
            status=QuizSessionStatus.PENDING_CONFIRM,
        )
        self._sessions.put(pending)
        return self.offer_message()

    async def resolve_offer(
        self,
        query: str,
        session_user: Optional[str] = None,
        token: Optional[str] = None,
        intent_type: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> CourseOffer:
        """Course-aware decision made AFTER a suitable learning answer.

        Returns one of:
          - OFF                -> not a learning context (nothing appended)
          - OFFER_QUIZ         -> enrolled & topic matches & not recently assessed
          - RECENTLY_ASSESSED  -> already assessed this course recently (no repeat)
          - RECOMMEND_COURSE   -> enrolment can't be confirmed -> delegate to
                                  the Course Recommendation service (no quiz)
        """
        suitability = self.evaluate_suitability(query, intent_type=intent_type, domain=domain)
        base = CourseOffer(
            suitable=suitability.suitable,
            topic=suitability.topic or "",
            reason=suitability.reason,
        )
        if not suitability.suitable:
            base.action = CourseOfferAction.OFF.value
            return base

        cfg = self._cfg()
        if not cfg.get("require_enrollment", True):
            # Legacy mode (enrollment not required) -> offer without a course gate.
            base.action = CourseOfferAction.OFFER_QUIZ.value
            return base

        # Unknown/absent token -> we cannot confirm enrolment, so stay conservative
        # and defer to course recommendations instead of offering a quiz.
        courses: List[Course] = []
        if self._course_context is not None:
            courses = await self._course_context.enrolled_courses(token)
        if not courses:
            base.action = CourseOfferAction.RECOMMEND_COURSE.value
            base.reason = "No enrolled course matching this topic."
            return base

        course = self._course_context.match_course(query, courses)
        if course is None:
            base.action = CourseOfferAction.RECOMMEND_COURSE.value
            base.reason = "Topic does not belong to an enrolled course."
            return base

        base.course = course
        base.course_slug = course.id

        profile = self._profiles.get_or_create(session_user or "anonymous")
        window = int(cfg.get("recent_window_seconds", 0))
        if window and self._course_context.recently_assessed(profile, course, window):
            base.action = CourseOfferAction.RECENTLY_ASSESSED.value
            base.reason = "Recently completed an assessment for this course."
            return base

        base.action = CourseOfferAction.OFFER_QUIZ.value
        base.reason = "Enrolled and topic maps to an in-progress course."
        return base


    def is_confirmation(self, text: str) -> bool:
        norm = _normalise(text)
        if not norm:
            return False
        # Word-boundary aware: "go" must not match "got", "yes" must not match
        # "yesterday". Padding with spaces keeps multi-word phrases contiguous.
        padded = f" {norm} "
        for phrase in _CONFIRMATION_PHRASES:
            if f" {_normalise(phrase)} " in padded:
                return True
        return False

    def is_decline(self, text: str) -> bool:
        norm = _normalise(text)
        for phrase in _DECLINE_PHRASES:
            if _normalise(phrase) in norm:
                return True
        return False

    def is_cancel(self, text: str) -> bool:
        norm = _normalise(text)
        for phrase in _CANCEL_PHRASES:
            if _normalise(phrase) in norm:
                return True
        return False

    def is_another_quiz(self, text: str) -> bool:
        norm = _normalise(text)
        for phrase in _ANOTHER_QUIZ_PHRASES:
            if _normalise(phrase) in norm:
                return True
        return False

    def resolve_difficulty(self, request: Optional[str]) -> DifficultyLevel:
        if request:
            parsed = self.parse_difficulty(request)
            if parsed:
                return parsed
        return DifficultyLevel(self._cfg().get("default_difficulty", "beginner"))

    # ---------------------------------------------------------------- lifecycle
    def get_session(self, session_key: str) -> Optional[QuizSession]:
        return self._sessions.get(session_key)

    async def start_quiz(
        self,
        session_key: str,
        topic: str,
        difficulty: Optional[DifficultyLevel] = None,
        count: Optional[int] = None,
        conversation: str = "",
        user_key: Optional[str] = None,
        course_slug: Optional[str] = None,
    ) -> Optional[str]:
        """Creates a quiz session, generates questions, returns the opening message."""

        cfg = self._cfg()
        length = max(1, min(count or cfg.get("default_length", 5), cfg.get("max_questions", 10)))
        level = difficulty or self.resolve_difficulty(None)
        topic = (topic or "cybersecurity").strip()

        previous_topics = self._profiles.get_previous_topics(user_key or session_key) if user_key else None

        questions = await self._generate_questions(
            topic=topic,
            difficulty=level.value,
            count=length,
            conversation=conversation,
            previous_topics=previous_topics,
        )
        if not questions:
            return None


        session = QuizSession(
            session_key=session_key,
            topic=topic,
            difficulty=level,
            length=len(questions),
            questions=questions,
            status=QuizSessionStatus.ACTIVE,
            metadata={"course_slug": course_slug} if course_slug else {},
        )
        self._sessions.put(session)
        self._record("assessment_started")
        self._events.started(session_key, topic, level.value)
        for q in questions:
            self._events.question_generated(session_key, q.question_id, q.type.value)

        current = session.current_question
        return self._format_opening(session, current)

    async def answer(self, session_key: str, answer_text: str) -> Optional[Dict[str, object]]:
        """Records an answer and returns the next turn payload."""
        session = self._sessions.get(session_key)
        if not session or not session.is_active:
            return None

        question = session.current_question
        if question is None:
            result = await self._finish(session)
            return {"kind": "summary", "message": self._format_summary(result, session)}

        correct, partial, feedback = await self._evaluate(question, answer_text)
        record = AnswerRecord(
            question_id=question.question_id,
            question_type=question.type,
            user_answer=answer_text,
            correct=correct,
            partial=partial,
            feedback=feedback,
            correct_answer=question.correct_answer,
            difficulty=question.difficulty,
            topic=question.topic,
        )
        session.answers.append(record)
        session.current_index += 1
        if self._cfg().get("adaptive") and correct:
            session.difficulty = self._adaptive_difficulty(session.difficulty)
        session.updated_at = datetime.utcnow()
        self._sessions.put(session)

        self._record("assessment_answered")
        self._events.answered(session_key, question.question_id, correct, partial)

        next_q = session.current_question
        if next_q is None:
            result = await self._finish(session)
            return {
                "kind": "summary",
                "message": self._format_feedback(feedback) + "\n\n" + self._format_summary(result, session),
                "result": result,
            }

        return {
            "kind": "next",
            "feedback": self._format_feedback(feedback),
            "message": self._format_feedback(feedback) + "\n\n" + self._format_question(next_q, session.current_index + 1, session.length),
            "question": next_q,
        }

    async def cancel(self, session_key: str) -> str:
        session = self._sessions.get(session_key)
        if session:
            session.status = QuizSessionStatus.ABANDONED
            self._sessions.put(session)
        return "No problem, I've stopped the quiz. Feel free to ask me anything else."

    async def clear_after(self, session_key: str) -> None:
        self._sessions.delete(session_key)

    # ------------------------------------------------------------------ internals
    async def _generate_questions(
        self,
        topic: str,
        difficulty: str,
        count: int,
        conversation: str,
        previous_topics: Optional[List[str]] = None,
    ) -> List[QuizQuestion]:
        question_types = self._select_question_types(topic)
        try:
            prompt = prompt_lib.build_generation_prompt(
                topic=topic,
                difficulty=difficulty,
                count=count,
                question_types=question_types,
                conversation=conversation,
                previous_topics=previous_topics,
            )
            raw = await self._llm.generate(
                prompt,
                system_prompt=prompt_lib.GENERATION_SYSTEM_PROMPT,
                temperature=0.7,
            )
            parsed = prompt_lib.parse_json(raw)
            questions = self._coerce_questions(parsed, topic, difficulty)
            if questions:
                return questions
        except Exception as exc:
            logger.warning("Assessment LLM generation failed, using fallback: %s", exc)

        return fallback_lib.generate_questions(topic, difficulty, count, question_types)

    def _select_question_types(self, topic: str) -> List[str]:
        text = topic.lower()
        types = list(_ALL_QUESTION_TYPES)
        if not any(k in text for k in ("python", "code", "sql", "javascript", "script")):
            types = [t for t in types if t != "code"]
        return types

    @staticmethod
    def _coerce_questions(parsed, topic: str, difficulty: str) -> List[QuizQuestion]:
        if not isinstance(parsed, list):
            return []
        questions: List[QuizQuestion] = []
        for item in parsed:
            if not isinstance(item, dict):
                continue
            qtype = str(item.get("type", "mcq")).lower()
            if qtype not in _ALL_QUESTION_TYPES:
                qtype = "mcq"
            try:
                questions.append(QuizQuestion(
                    type=QuestionType(qtype),
                    text=str(item.get("text", "")).strip(),
                    options=[str(o) for o in (item.get("options") or [])],
                    correct_answer=str(item.get("correct_answer", "")).strip(),
                    explanation=str(item.get("explanation", "")).strip(),
                    difficulty=DifficultyLevel(difficulty),
                    topic=str(item.get("topic") or topic),
                ))
            except Exception:
                continue
        return questions

    async def _evaluate(self, question: QuizQuestion, user_answer: str) -> tuple:
        if question.type in (QuestionType.MCQ, QuestionType.TRUE_FALSE, QuestionType.FILL_IN_BLANK):
            return fallback_lib.evaluate_fallback(question, user_answer)

        try:
            prompt = prompt_lib.build_evaluation_prompt(
                question=question.text,
                options=question.options,
                correct_answer=question.correct_answer,
                user_answer=user_answer,
            )
            raw = await self._llm.generate(
                prompt,
                system_prompt=prompt_lib.EVALUATION_SYSTEM_PROMPT,
                temperature=0.2,
            )
            parsed = prompt_lib.parse_json(raw)
            if isinstance(parsed, dict) and "correct" in parsed:
                return (
                    bool(parsed.get("correct", False)),
                    bool(parsed.get("partial", False)),
                    str(parsed.get("feedback", "")).strip(),
                )
        except Exception as exc:
            logger.warning("Assessment LLM evaluation failed, using fallback: %s", exc)

        return fallback_lib.evaluate_fallback(question, user_answer)

    async def _build_result(self, session: QuizSession) -> QuizResult:
        score = sum(1 for a in session.answers if a.correct)
        total = len(session.answers)
        passed = total > 0 and (score / total) >= _PASS_THRESHOLD

        try:
            qa_pairs = "\n".join(
                f"Q: {q.text}\nA: {a.user_answer}\nExpected: {a.correct_answer or 'open-ended'}\n"
                for q, a in zip(session.questions, session.answers)
            )
            raw = await self._llm.generate(
                prompt_lib.build_summary_prompt(session.topic, qa_pairs),
                system_prompt=prompt_lib.SUMMARY_SYSTEM_PROMPT,
                temperature=0.4,
            )
            parsed = prompt_lib.parse_json(raw)
            if isinstance(parsed, dict):
                strengths = _as_list(parsed.get("strengths"))
                weak = _as_list(parsed.get("weak_areas"))
                recommendations = _as_list(parsed.get("recommendations"))
                next_topic = str(parsed.get("next_topic", "")).strip()
            else:
                raise ValueError("summary did not parse")
        except Exception as exc:
            logger.warning("Assessment LLM summary failed, using fallback: %s", exc)
            fallback_data = fallback_lib.build_summary_fallback(
                session.questions, session.answers, session.topic
            )
            strengths, weak = fallback_data["strengths"], fallback_data["weak_areas"]
            recommendations = fallback_data["recommendations"]
            next_topic = fallback_data["next_topic"]

        return QuizResult(
            score=score,
            total=total,
            passed=passed,
            strengths=strengths,
            weak_areas=weak,
            recommendations=recommendations,
            next_topic=next_topic,
            difficulty_reached=session.difficulty,
        )

    async def _finish(self, session: QuizSession) -> QuizResult:
        result = await self._build_result(session)
        session.status = QuizSessionStatus.COMPLETED
        self._sessions.put(session)

        user_key = session.session_key
        course_slug = session.metadata.get("course_slug") if session.metadata else None
        self._profiles.record_result(user_key, result, session.topic, course_slug=course_slug)
        profile = self._profiles.get_or_create(user_key)

        self._record("assessment_completed")
        self._events.completed(session.session_key, result.score, result.total, result.passed)
        self._events.learning_progress(
            session.session_key, profile.topics_completed, profile.average_score
        )
        return result

    def _adaptive_difficulty(self, current: DifficultyLevel) -> DifficultyLevel:
        order = list(DifficultyLevel)
        try:
            idx = order.index(current)
            if idx < len(order) - 1:
                return order[idx + 1]
        except ValueError:
            pass
        return current

    def _record(self, metric: str):
        if self._obs is not None:
            try:
                self._obs.increment_counter(f"assessment.{metric}", 1)
            except Exception:
                pass

    # ------------------------------------------------------------------ formatting
    def _format_opening(self, session: QuizSession, question: QuizQuestion) -> str:
        return (
            "Great! Let's begin.\n\n"
            + self._format_question(question, 1, session.length)
        )

    @staticmethod
    def _format_question(question: QuizQuestion, index: int, total: int) -> str:
        lines = [f"**Question {index} of {total}**", f"{question.text}"]
        if question.options:
            for i, opt in enumerate(question.options):
                lines.append(f"{chr(ord('A') + i)}. {opt}")
        return "\n".join(lines)

    @staticmethod
    def _format_feedback(feedback: str) -> str:
        return feedback.strip()

    @staticmethod
    def _format_summary(result: QuizResult, session: QuizSession) -> str:
        strength_line = "\n".join(f"- {s}" for s in result.strengths) or "- Keep practicing"
        weak_line = "\n".join(f"- {w}" for w in result.weak_areas) or "- Review the material"
        rec_line = "\n".join(f"- {r}" for r in result.recommendations) or "- Keep going"
        next_topic = result.next_topic or "a related advanced topic"

        lines = [
            f"Quiz complete! You scored **{result.score} / {result.total}**.",
            "",
            "**Strengths**",
            strength_line,
            "",
            "**Needs Improvement**",
            weak_line,
            "",
            "**Learning Recommendations**",
            rec_line,
            "",
            f"**Recommended Next Topic**",
            f"- {next_topic}",
            "",
            "You can ask for another quiz on any topic anytime.",
        ]
        return "\n".join(lines)


def _as_list(value) -> List[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return [str(value).strip()]
