import json
import logging
from typing import List, Optional

from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.platform.repositories.interfaces import IPlatformRepository
from app.platform.context.user_context import UserContextBuilder
from app.platform.services.recommendation_service import RecommendationService
from app.rag.interfaces import IRetriever
from app.llm.interfaces import ILLMService
from app.prompt_builder.interfaces import IPromptBuilder
from app.chat.intent.models.intent_types import IntentType
from app.chat.engines.citations import build_citations
from app.chat.engines.course_sources import build_course_sources

logger = logging.getLogger("app.chat.engines.platform_engine")

_RECOMMEND_QUERY_WORDS = ("recommend", "suggest", "should", "which course", "next course", "best course")

# Queries that ask for course guidance but don't use an explicit recommendation
# verb ("i want courses for beginner", "where do i start", ...). They should be
# answered with content-grounded recommendations, not just the enrolled list.
_COURSE_LEVEL_SIGNALS = (
    "beginner", "intermediate", "advanced", "for beginners", "for a beginner",
    "where do i start", "start with", "how to start", "i want to learn",
    "i'm new", "im new", "just starting", "learning path",
)

_PURE_PLATFORM_INTENTS = {
    IntentType.PLATFORM_COURSE,
    IntentType.PLATFORM_PROGRESS,
    IntentType.PLATFORM_CERTIFICATE,
    IntentType.PLATFORM_ASSESSMENT,
    IntentType.PLATFORM_PROFILE,
    IntentType.PLATFORM_DASHBOARD,
    IntentType.PLATFORM_BADGE,
    IntentType.PLATFORM_LEARNING_PATH,
    IntentType.PLATFORM_LAB,
}

# Queries that refer to the page the learner is currently viewing ("this
# course", "this page", ...). When a course page context is present they should
# be answered about THAT course, not with the generic enrolled-courses list.
_PAGE_REFERENCE_SIGNALS = (
    "this course", "this one", "this page", "the course i'm viewing",
    "the course im viewing", "the course i am viewing", "what is this course",
    "about this course", "tell me about this course", "explain this course",
    "explain about this course",
)


class PlatformExecutionEngine(IExecutionEngine):
    """
    Intent-aware Platform Engine.
    Executes PLATFORM_* intents by fetching deterministic data from the Platform
    Repository (enrolled courses, progress, certificates, assessments, profile)
    and uses the LLM only when reasoning is actually required (e.g. interpreting
    data against a goal). Pure data-fetch and recommendation intents are answered
    deterministically WITHOUT calling the LLM.
    """
    def __init__(
        self, 
        platform_repo: IPlatformRepository, 
        user_context_builder: UserContextBuilder,
        recommendation_service: RecommendationService,
        retriever: IRetriever,
        llm_service: ILLMService, 
        prompt_builder: IPromptBuilder
    ):
        self._repo = platform_repo
        self._user_context_builder = user_context_builder
        self._recommendation_service = recommendation_service
        self._retriever = retriever
        self._llm = llm_service
        self._prompt_builder = prompt_builder

    @property
    def name(self) -> str:
        return "PLATFORM"

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        query = context.metadata.get("query", "")
        token = context.metadata.get("token")
        intent = self._extract_intent(context)

        # If the learner refers to the page they're on ("this course") and a
        # course page context is present, describe THAT course instead of the
        # generic enrolled-courses list.
        if self._is_page_reference(query):
            page_course = self._page_course_slug(context)
            if page_course:
                try:
                    info = await self._build_course_description(page_course, token)
                except Exception as e:
                    logger.warning(f"Course-description build failed for {page_course}: {e}")
                    info = None
                if info:
                    platform_metadata = {
                        "platform": {
                            "cards": [],
                            "actions": [],
                            "context_used": info["context_used"],
                        },
                        "agent": "platform_assistant",
                        "engine": "PLATFORM",
                        "platform_cards": [],
                        "actions": [],
                        "recommendation_used": False,
                        "llm_used": False,
                        "repositories": ["platform_repository"],
                        "intent": context.metadata.get("intent", ""),
                        "domain": context.metadata.get("domain", ""),
                        "course_info": info,
                        "suggested_courses": [],
                    }
                    return ExecutionResult.success(
                        engine=self.name,
                        message=self._format_course_description(info),
                        metadata=platform_metadata,
                        documents=[],
                    )

        # 1. Platform data retrieval (deterministic, intent-driven)
        platform_data = await self._collect_platform_data(intent, query, token, context)

        # 2. Build cards + metadata for the UI
        platform_cards, actions = self._build_platform_ui(platform_data)
        recommendation_used = bool(platform_data.get("recommendations"))
        platform_metadata = {
            "platform": {
                "cards": platform_cards,
                "actions": actions,
                "context_used": platform_data.get("context_used", []),
            },
            "agent": "platform_assistant",
            "engine": "PLATFORM",
            "platform_cards": platform_cards,
            "actions": actions,
            "recommendation_used": recommendation_used,
            "repositories": ["platform_repository"],
            "intent": context.metadata.get("intent", ""),
            "domain": context.metadata.get("domain", ""),
        }

        # 3. RAG Retrieval only for knowledge-seeking queries. Pure platform
        # intents (progress/certificates/assessments/profile) are answered
        # entirely from Django data, so retrieval would only add confusing
        # citations. Course-suggestion queries DO retrieve: the answer must be
        # grounded in actual BlueTeamers lesson content so the recommendation
        # can point to real lessons.
        recommendation_mode = bool(platform_data.get("wants_recommendation"))
        documents = []
        if intent not in _PURE_PLATFORM_INTENTS or recommendation_mode:
            try:
                top_k = 8 if recommendation_mode else 3
                documents = await self._retriever.search(query, top_k=top_k)
            except Exception as e:
                logger.warning(f"Platform engine RAG retrieval failed: {e}")
        doc_contexts = [{"content": d.content, "metadata": d.metadata} for d in documents]
        platform_metadata["sources"] = doc_contexts

        # 3b. Course Source Cards: emit automatically whenever the answer is
        # grounded in BlueTeamers lesson chunks (progress when already fetched),
        # plus any clickable lesson cards derived from course recommendations.
        progress_by_slug = {p.course_slug: p.percent_complete for p in platform_data.get("progress", [])}
        course_sources = build_course_sources(documents, progress_by_slug=progress_by_slug or None)
        rec_sources = platform_data.get("recommended_course_sources") or []
        if rec_sources:
            # Merge, deduplicating by course so a course appears once (lesson
            # cards from RAG are more specific, so they win over rec placeholders).
            seen = {s.get("course_slug") or s.get("course_id") for s in course_sources if s.get("course_slug") or s.get("course_id")}
            merged = list(course_sources)
            for s in rec_sources:
                key = s.get("course_slug") or s.get("course_id")
                if key and key not in seen:
                    merged.append(s)
                    seen.add(key)
            course_sources = merged
        platform_metadata["course_sources"] = course_sources

        # 4a. NO-LLM path: pure data-fetch intents are answered deterministically
        # from the fetched platform data. Recommendation/suggestion queries are
        # NOT pure — they need the LLM to explain the "why" using the retrieved
        # lesson content (step 4b).
        if intent in _PURE_PLATFORM_INTENTS and not recommendation_mode:
            content = self._build_structured_content(platform_data, intent)
            platform_metadata["llm_used"] = False
            return ExecutionResult.success(
                engine=self.name,
                message=content,
                metadata=platform_metadata,
                documents=doc_contexts,
                citations=build_citations(documents),
            )

        # 4b. LLM reasoning path: strict system instruction bound to the actual
        # platform data (and, for recommendations, to retrieved course content).
        platform_metadata["llm_used"] = True
        system_instruction = self._build_system_instruction(
            platform_data, intent, doc_contexts=doc_contexts
        )

        enhanced_context = {
            **context.memory,
            "retrieved_documents": doc_contexts,
            "platform_system_instruction": system_instruction,
        }

        prompt, builder_system_prompt = self._prompt_builder.build_prompt(query, enhanced_context)
        combined_system = f"{builder_system_prompt}\n\n{system_instruction}"

        # 5. LLM Execution (summarizes only the provided platform data)
        images = context.metadata.get("images")
        if context.streaming_mode:
            generator = self._llm.stream(prompt, system_prompt=combined_system, images=images)
            return ExecutionResult.success(
                engine=self.name,
                message="[Streaming Generator]",
                metadata={"generator": generator, **platform_metadata},
                documents=doc_contexts,
                citations=build_citations(documents)
            )
        else:
            response = await self._llm.generate(prompt, system_prompt=combined_system, images=images)
            if not response or len(response.strip()) <= 2:
                logger.warning(
                    "LLM returned degenerate response for intent=%s (len=%s); "
                    "falling back to structured content",
                    intent,
                    len(response or ""),
                )
                response = self._build_structured_content(platform_data, intent)
                platform_metadata["llm_used"] = False
            return ExecutionResult.success(
                engine=self.name,
                message=response,
                metadata=platform_metadata,
                documents=doc_contexts,
                citations=build_citations(documents)
            )

    @staticmethod
    def _extract_intent(context: ExecutionContext) -> Optional[IntentType]:
        analysis = context.metadata.get("intent_analysis")
        if analysis and getattr(analysis, "primary_intent", None):
            return analysis.primary_intent.type
        return None

    @staticmethod
    def _page_course_slug(context: ExecutionContext) -> Optional[str]:
        """Resolve the course the learner is currently viewing, from the
        frontend's ``request.context.page`` payload (e.g. a course page)."""
        req_context = context.metadata.get("context")
        if not isinstance(req_context, dict):
            return None
        page = req_context.get("page")
        if not isinstance(page, dict):
            return None
        if str(page.get("type", "")).lower() != "course":
            return None
        slug = page.get("course") or page.get("course_slug")
        return str(slug) if slug else None

    @staticmethod
    def _is_page_reference(query: str) -> bool:
        q = query.lower()
        return any(sig in q for sig in _PAGE_REFERENCE_SIGNALS)

    async def _build_course_description(
        self, course_slug: str, token: Optional[str]
    ) -> dict:
        """Describe the specific BlueTeamers course the learner is viewing.

        Uses the static catalog for public metadata (title, description,
        difficulty, duration, module titles) and, when the learner is enrolled,
        their live progress. Never exposes lesson bodies for not-enrolled.
        """
        from app.knowledge.sources import load_course_catalog
        from app.chat.engines.course_sources import _LEVEL_LABELS

        catalog = load_course_catalog()
        meta = catalog.get(course_slug, {})
        title = meta.get("title") or course_slug
        level_raw = str(meta.get("difficulty", "") or "")
        level = _LEVEL_LABELS.get(level_raw.lower(), level_raw.title() if level_raw else "Beginner")
        duration = str(meta.get("duration") or "N/A")
        modules = []
        for module in meta.get("modules", []):
            lessons = [str(lesson.get("title", "")) for lesson in module.get("lessons", []) if lesson.get("title")]
            modules.append({"title": str(module.get("title", "")), "lessons": lessons})

        enrolled = False
        progress_pct = None
        context_used = ["course-catalog"]
        if token:
            try:
                enrolled_courses = await self._repo.get_enrolled_courses(token)
                enrolled = any(c.id == course_slug for c in enrolled_courses)
                if enrolled:
                    context_used = ["course-catalog", "enrolled-courses"]
                    try:
                        prog = await self._repo.get_progress(course_slug, token)
                    except Exception as e:
                        logger.warning(f"Course-description progress fetch failed for {course_slug}: {e}")
                        prog = None
                    if prog and prog.percent_complete is not None:
                        progress_pct = int(prog.percent_complete)
                        context_used.append("progress")
            except Exception as e:
                logger.warning(f"Course-description enrollment fetch failed for {course_slug}: {e}")

        return {
            "title": title,
            "course_slug": course_slug,
            "description": meta.get("description") or "",
            "level": level,
            "duration": duration,
            "modules": modules,
            "enrolled": bool(enrolled),
            "progress": progress_pct,
            "context_used": context_used,
        }

    async def _collect_platform_data(self, intent, query: str, token: str, context) -> dict:
        data = {
            "profile": None,
            "enrolled": [],
            "progress": [],
            "certificates": [],
            "assessments": [],
            "recommendations": [],
            "unavailable": False,
            "context_used": [],
        }

        if not token:
            routing_decision = context.metadata.get("routing_decision")
            domain = getattr(routing_decision, "domain", None) if routing_decision else None
            data["is_guest"] = True
            if intent == IntentType.PLATFORM_COURSE:
                # Guests can't be shown live enrollments/progress, but they can
                # still be recommended BlueTeamers catalog courses and invited to
                # enroll (no Django call required).
                data["wants_recommendation"] = True
                data["recommendations"] = await self._recommendation_service.generate_from_catalog(
                    query=query, domain=domain
                )
                data["recommended_course_sources"] = self._recs_to_course_sources(
                    data["recommendations"]
                )
                data["context_used"] = ["catalog-recommendations"]
            else:
                data["unavailable"] = True
            return data

        # A deterministic guard: only touch Django when the intent actually needs platform data.
        try:
            if intent in (IntentType.PLATFORM_PROFILE, IntentType.PLATFORM_DASHBOARD):
                data["profile"] = await self._repo.get_user_profile(token)
                data["context_used"].append("profile")

            if intent in (
                IntentType.PLATFORM_COURSE,
                IntentType.PLATFORM_PROGRESS,
                IntentType.PLATFORM_CERTIFICATE,
                IntentType.PLATFORM_ASSESSMENT,
                IntentType.PLATFORM_DASHBOARD,
                IntentType.PLATFORM_LAB,
            ):
                data["enrolled"] = await self._repo.get_enrolled_courses(token)
                data["context_used"].append("enrolled-courses")

            if intent in (IntentType.PLATFORM_PROGRESS, IntentType.PLATFORM_DASHBOARD):
                for course in data["enrolled"]:
                    try:
                        p = await self._repo.get_progress(course.id, token)
                    except Exception as e:
                        logger.warning(f"Progress fetch failed for {course.id}: {e}")
                        p = None
                    if p:
                        data["progress"].append(p)
                data["context_used"].append("progress")

            if intent in (IntentType.PLATFORM_CERTIFICATE, IntentType.PLATFORM_DASHBOARD):
                data["certificates"] = await self._repo.get_certificates(token)
                data["context_used"].append("certificates")

            if intent in (IntentType.PLATFORM_ASSESSMENT, IntentType.PLATFORM_DASHBOARD):
                for course in data["enrolled"]:
                    try:
                        data["assessments"].extend(
                            await self._repo.get_assessments(course.id, token)
                        )
                    except Exception as e:
                        logger.warning(f"Assessment fetch failed for {course.id}: {e}")
                data["context_used"].append("assessments")

            # Course recommendations: triggered by explicit recommendation phrasing,
            # by beginner/level guidance phrasing, or as a fallback when the user
            # has no enrollments. Relevance is driven by the classified cyber
            # domain (not query keyword matching). These queries are answered via
            # the LLM grounded in retrieved BlueTeamers lesson content so the
            # response references real lessons, not just a flat list.
            routing_decision = context.metadata.get("routing_decision")
            domain = getattr(routing_decision, "domain", None) if routing_decision else None
            wants_recommendation = intent == IntentType.PLATFORM_COURSE and (
                any(w in query.lower() for w in _RECOMMEND_QUERY_WORDS)
                or any(sig in query.lower() for sig in _COURSE_LEVEL_SIGNALS)
                or not data["enrolled"]
            )
            data["wants_recommendation"] = wants_recommendation
            if wants_recommendation:
                data["recommendations"] = await self._recommendation_service.generate_for_domain(
                    token,
                    domain=domain,
                    exclude_slugs=[c.id for c in data["enrolled"]],
                    query=query,
                )
                # Build clickable lesson cards from the grey recommendations so the
                # frontend renders CourseSourceCards with direct lesson links.
                data["recommended_course_sources"] = self._recs_to_course_sources(
                    data["recommendations"]
                )
                data["context_used"].append("recommendations")

            if intent in (
                IntentType.PLATFORM_LEARNING_PATH,
                IntentType.PLATFORM_BADGE,
                IntentType.PLATFORM_LAB,
            ):
                data["context_used"].append("unavailable-feature")

        except Exception as e:
            logger.error(f"Platform data collection failed: {e}")
            data["unavailable"] = True

        return data

    @staticmethod
    def _build_platform_ui(data: dict) -> tuple:
        cards = []
        actions = []
        progress_by_slug = {p.course_slug: p.percent_complete for p in data.get("progress", [])}
        enrolled_slugs = {c.id for c in data.get("enrolled", [])}

        for course in data.get("enrolled", []):
            pct = progress_by_slug.get(course.id, 0)
            cards.append({
                "title": course.title,
                "type": "course",
                "difficulty": course.level,
                "duration": f"{course.duration_hours}h",
                "description": course.description or "",
                "progress": f"{pct}%",
                "action": {
                    "label": "Go to course",
                    "action_type": "open_course",
                    "payload": {"id": course.id, "url": f"/courses/{course.id}"},
                },
                "actions": [
                    {
                        "label": "Go to course",
                        "action_type": "open_course",
                        "payload": {"id": course.id, "url": f"/courses/{course.id}"},
                    },
                    {
                        "label": "Course info",
                        "action_type": "course_info",
                        "payload": {"id": course.id},
                    },
                ],
            })

        for rec in data.get("recommendations", []):
            if rec.item_id in enrolled_slugs:
                continue
            cards.append({
                "title": rec.title,
                "type": rec.type,
                "difficulty": rec.difficulty,
                "duration": "N/A",
                "description": rec.reason or "",
                "progress": "",
                "action": {
                    "label": "Enroll course",
                    "action_type": "enroll_course",
                    "payload": {"id": rec.item_id, "url": f"/courses/{rec.item_id}/checkout"},
                },
                "actions": [
                    {
                        "label": "Enroll course",
                        "action_type": "enroll_course",
                        "payload": {"id": rec.item_id, "url": f"/courses/{rec.item_id}/checkout"},
                    },
                    {
                        "label": "Go to course",
                        "action_type": "open_course",
                        "payload": {"id": rec.item_id, "url": f"/courses/{rec.item_id}"},
                    },
                    {
                        "label": "Course info",
                        "action_type": "course_info",
                        "payload": {"id": rec.item_id},
                    },
                ],
            })

        for cert in data.get("certificates", []):
            actions.append({
                "label": f"View certificate - {cert.course_slug}",
                "action_type": "view_certificate",
                "payload": {"id": cert.id, "url": f"/verify/{cert.id}"},
            })
        return cards, actions

    @staticmethod
    def _recs_to_course_sources(recs) -> list:
        """Convert Recommendation objects into CourseSourceCard-shaped metadata.

        Each recommended course becomes a card carrying direct lesson deep-links,
        so the frontend renders clickable ``CourseSourceCard`` components (the
        same cards used for RAG-grounded answers).
        """
        sources = []
        for index, rec in enumerate(recs):
            slug = rec.course_slug or rec.item_id
            lessons = rec.lessons or []
            sources.append({
                "course_slug": slug,
                "course_id": rec.item_id,
                "title": rec.title,
                "label": "Recommended for You",
                "rank": index + 1,
                "lessons": lessons,
                "lessons_count": len(lessons),
                "progress": None,
                "duration": "N/A",
                "level": rec.level or rec.difficulty,
                "reason": rec.reason,
                "action": {
                    "label": "Start Learning",
                    "url": rec.lesson_url or (f"/courses/{slug}" if not lessons else ""),
                },
                "course_action": {
                    "label": "View Course",
                    "url": rec.course_url or f"/courses/{slug}",
                },
            })
        return sources

    @staticmethod
    def _format_course_description(info: dict) -> str:
        """Human-friendly course overview for the page the learner is viewing."""
        lines = [f"**{info['title']}**"]
        meta = f"{info['level']} · {info['duration']}"
        if info.get("enrolled") and info.get("progress") is not None:
            meta += f" · {info['progress']}% complete"
        lines.append(meta)
        if info.get("description"):
            lines.append("")
            lines.append(info["description"])
        modules = info.get("modules") or []
        if modules:
            lines.append("")
            lines.append("**What you'll learn:**")
            for m in modules:
                lines.append(f"- {m['title']} ({len(m['lessons'])} lessons)")
        if info.get("enrolled"):
            lines.append("")
            lines.append("You're enrolled in this course. Ask me to explain any topic, "
                         "module, or lesson, or say 'take the next lesson' to continue.")
        else:
            lines.append("")
            lines.append("Enroll in this course to unlock the lessons and start learning.")
        return "\n".join(lines)

    def _build_structured_content(self, data: dict, intent) -> str:
        """Deterministic answer for pure platform intents — no LLM involved."""
        if data.get("is_guest"):
            recs = data.get("recommendations", [])
            if recs:
                lines = ["Here are some BlueTeamers courses you can take:"]
                for r in recs:
                    lines.append(f"  - {r.title}: {r.reason}")
                lines.append(
                    "Log in and join a course to start learning — which one would "
                    "you like to take?"
                )
                return "\n".join(lines)
            return (
                "You're browsing as a guest. Log in to see your enrolled courses, "
                "progress, and certificates. Meanwhile, I can recommend BlueTeamers "
                "courses — just ask!"
            )

        if data.get("unavailable") or not data.get("context_used"):
            return (
                "I couldn't reach the BlueTeamers platform service right now, so I "
                "can't pull your live courses, progress, or certificates. Please try "
                "again in a moment."
            )

        lines = []
        profile = data.get("profile")
        if profile and (profile.full_name or profile.email):
            lines.append(f"You're signed in as {profile.full_name or profile.email}.")

        enrolled = data.get("enrolled", [])
        progress_by_slug = {p.course_slug: p.percent_complete for p in data.get("progress", [])}
        if intent in (IntentType.PLATFORM_COURSE, IntentType.PLATFORM_PROGRESS, IntentType.PLATFORM_DASHBOARD):
            if enrolled:
                lines.append("Your enrolled courses:")
                for c in enrolled:
                    pct = progress_by_slug.get(c.id, 0)
                    lines.append(f"  - {c.title} ({pct}% complete)")
            else:
                lines.append("You're not enrolled in any courses yet.")

        recs = data.get("recommendations", [])
        if recs:
            lines.append("Courses I'd recommend:")
            for r in recs:
                lines.append(f"  - {r.title}: {r.reason}")

        certs = data.get("certificates", [])
        if intent in (IntentType.PLATFORM_CERTIFICATE, IntentType.PLATFORM_DASHBOARD):
            if certs:
                lines.append("Your certificates:")
                for cert in certs:
                    lines.append(f"  - {cert.course_slug} (issued {cert.issued_at or 'recently'})")
            else:
                lines.append("You don't have any certificates yet.")

        assessments = data.get("assessments", [])
        if intent in (IntentType.PLATFORM_ASSESSMENT, IntentType.PLATFORM_DASHBOARD):
            if assessments:
                lines.append("Your assessment scores:")
                for a in assessments:
                    verdict = "passed" if a.passed else "not passed"
                    lines.append(f"  - {a.title}: {a.score}/100 ({verdict})")
            else:
                lines.append("No assessment scores are available yet.")

        if intent in (IntentType.PLATFORM_BADGE, IntentType.PLATFORM_LEARNING_PATH, IntentType.PLATFORM_LAB):
            lines.append("Badges, learning paths, and labs are not available on the platform yet.")

        return "\n".join(lines) if lines else "I don't have any platform information to show you yet."

    def _build_system_instruction(self, data: dict, intent, doc_contexts=None) -> str:
        if data.get("is_guest") and intent == IntentType.PLATFORM_COURSE:
            recs = [{"title": r.title, "reason": r.reason, "type": r.type} for r in data.get("recommendations", [])]
            parts = [
                "The user is browsing as a guest (not logged in).",
                "You MUST answer strictly from the 'Recommended items' and 'BlueTeamers Content' below. "
                "NEVER invent courses, and NEVER reference external vendors like CompTIA, SANS, or Coursera.",
                f"Recommended items: {json.dumps(recs)}",
            ]
            if doc_contexts:
                parts.append(
                    "BlueTeamers Content (retrieved from BlueTeamers' own lessons): "
                    + json.dumps(
                        [
                            {
                                "course": (d.get("metadata") or {}).get("course_title"),
                                "course_slug": (d.get("metadata") or {}).get("course_slug"),
                                "lesson": (d.get("metadata") or {}).get("lesson_title"),
                                "lesson_id": (d.get("metadata") or {}).get("lesson_id"),
                                "module": (d.get("metadata") or {}).get("module_title"),
                                "snippet": (d.get("content") or "")[:220],
                            }
                            for d in doc_contexts[:12]
                        ],
                        default=str,
                    )
                )
            parts.append(
                "The user asked for course suggestions. Keep your answer SHORT (2-4 "
                "sentences): recommend 2-3 BlueTeamers courses with a one-line reason "
                "each, then invite them to take a course (e.g. 'Enroll in X to get "
                "started'). Do NOT dump the full list or extra detail."
            )
            return "\n".join(parts)

        if data.get("unavailable") or not data.get("context_used"):
            if data.get("is_guest"):
                return (
                    "The user is browsing as a guest. Their account data is not "
                    "available. Do NOT invent courses, progress, or certificates. "
                    "Tell them to log in to see their account data, and invite them "
                    "to ask for BlueTeamers course suggestions."
                )
            return (
                "The BlueTeamers platform service is currently unavailable, so no live "
                "course, progress, or certificate data could be retrieved. Do NOT invent "
                "or recommend any courses, labs, or progress. Briefly apologize and tell "
                "the user that live data is temporarily unavailable and to try again shortly."
            )

        recommendation_mode = bool(data.get("wants_recommendation"))

        parts = [
            "The user is asking about their BlueTeamers platform account.",
            "You MUST answer strictly from the 'Platform Data' and 'BlueTeamers Content' below. "
            "NEVER invent courses, progress, certificates, or scores that are not listed here. "
            "Do NOT reference external vendors like CompTIA, SANS, or Coursera.",
        ]

        profile = data.get("profile")
        if profile and (profile.full_name or profile.email):
            parts.append(f"User name/email: {profile.full_name or profile.email}")

        enrolled = data.get("enrolled", [])
        if recommendation_mode:
            recs = [{"title": r.title, "reason": r.reason, "type": r.type} for r in data.get("recommendations", [])]
            parts.append(f"Recommended items: {json.dumps(recs)}")
            if doc_contexts:
                parts.append(
                    "BlueTeamers Content (retrieved from BlueTeamers' own lessons): "
                    + json.dumps(
                        [
                            {
                                "course": (d.get("metadata") or {}).get("course_title"),
                                "course_slug": (d.get("metadata") or {}).get("course_slug"),
                                "lesson": (d.get("metadata") or {}).get("lesson_title"),
                                "lesson_id": (d.get("metadata") or {}).get("lesson_id"),
                                "module": (d.get("metadata") or {}).get("module_title"),
                                "snippet": (d.get("content") or "")[:220],
                            }
                            for d in doc_contexts[:12]
                        ],
                        default=str,
                    )
                )
            parts.append(
                "The user is asking for course suggestions. Recommend courses that fit "
                "their level (e.g. beginner), and where possible tie each recommendation "
                "to the actual BlueTeamers lessons from 'BlueTeamers Content' (name the "
                "course, module, and lesson). Keep it short and friendly."
            )
        if enrolled:
            parts.append(f"Enrolled courses: {json.dumps([{'title': c.title, 'slug': c.id} for c in enrolled])}")
        else:
            parts.append("Enrolled courses: None.")

        progress = data.get("progress", [])
        if progress:
            parts.append(
                "Progress: "
                + json.dumps([{"course": p.course_slug, "percent": p.percent_complete, "lessons_completed": len(p.completed_lessons)} for p in progress])
            )

        certs = data.get("certificates", [])
        if certs:
            parts.append(f"Certificates: {json.dumps([{'course': c.course_slug, 'issued': c.issued_at} for c in certs])}")

        assessments = data.get("assessments", [])
        if assessments:
            parts.append(
                "Assessment scores: "
                + json.dumps([{"quiz": a.title, "score": a.score, "passed": a.passed} for a in assessments])
            )

        if intent in (IntentType.PLATFORM_BADGE, IntentType.PLATFORM_LEARNING_PATH):
            parts.append("Badges/Learning Paths are not yet available on this platform. Say so honestly if asked.")

        return "\n".join(parts)
