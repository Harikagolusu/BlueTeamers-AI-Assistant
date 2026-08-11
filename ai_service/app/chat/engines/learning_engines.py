"""Text-only learning engines for the AI Cybersecurity Learning Assistant.

These engines produce structured markdown in the chat response itself — no
cards, quizzes, or interactive UI. They reuse the existing RAG retriever,
LLM service, prompt builder, and platform repository:

- NotesGenerationEngine  -> "generate notes", "revision notes", "cheat sheet"
- TopicSummaryEngine     -> "summarize this topic", "TL;DR", "quick revision"

Each engine searches the learner's enrolled course material first and falls
back to the general knowledge base (course-first retrieval), mirroring the
Course Material Q&A behaviour of RagExecutionEngine.
"""

import logging

from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.rag.interfaces import IRetriever
from app.llm.interfaces import ILLMService
from app.prompt_builder.interfaces import IPromptBuilder
from app.chat.engines.agent_backed_engine import AgentBackedEngine
from app.chat.engines.course_sources import _LEVEL_LABELS
from app.knowledge.sources import load_course_catalog

logger = logging.getLogger("app.chat.engines.learning_engines")


def _document_metadata(doc) -> dict:
    if isinstance(doc, dict):
        return doc.get("metadata") or {}
    return getattr(doc, "metadata", None) or {}


class CourseFirstAgentEngine(AgentBackedEngine):
    """AgentBackedEngine that prioritizes the learner's enrolled course
    material before falling back to the general knowledge base.

    Content-generation subclasses (Notes / Summary) can opt into course-aware
    access control via ``gate_course_content = True``: when the requested topic
    is covered by a BlueTeamers course the learner is NOT enrolled in, the
    engine returns a short overview + course recommendation card instead of
    reproducing the full course material.
    """

    #: Opt-in course-aware gate. SOC specialist engines keep this off so their
    #: mentoring/analysis answers (event IDs, labs, log triage) are unchanged.
    gate_course_content = False

    def __init__(
        self,
        retriever: IRetriever,
        llm_service: ILLMService,
        prompt_builder: IPromptBuilder,
        platform_repo=None,
    ):
        super().__init__(retriever, llm_service, prompt_builder)
        self._platform_repo = platform_repo

    async def _resolve_enrolled_slugs(self, context: ExecutionContext) -> set:
        """Best-effort resolution of enrolled course slugs. Never raises."""
        if not self._platform_repo:
            return set()
        token = context.metadata.get("token")
        if not token:
            return set()
        try:
            enrolled = await self._platform_repo.get_enrolled_courses(token)
            return {c.id for c in enrolled}
        except Exception as e:
            logger.warning(f"Enrolled-course resolution failed: {e}")
            return set()

    async def _retrieve(self, query: str, context: ExecutionContext, enrolled_slugs=None):
        """Course-material-first retrieval with general knowledge fallback.

        ``enrolled_slugs`` may be passed in to avoid a duplicate platform call
        when the caller already resolved it (e.g. the course-access gate).
        """
        if enrolled_slugs is None:
            enrolled_slugs = await self._resolve_enrolled_slugs(context)
        if not enrolled_slugs:
            return await self._retriever.search(query, top_k=self.top_k), "general"

        course_docs = await self._retriever.search(
            query,
            top_k=self.top_k,
            metadata_filters={
                "source": "lesson_content",
                "course_slug": list(enrolled_slugs),
            },
        )
        if course_docs:
            return course_docs, "course"

        return await self._retriever.search(query, top_k=self.top_k), "general"

    async def execute(self, context: ExecutionContext):
        """Course-aware gate: only full course content for enrolled learners.

        When ``gate_course_content`` is enabled and the topic belongs to a
        course the learner has not enrolled in, generate a short overview with
        a course recommendation instead of full notes/summary. Everything else
        (enrolled course content, general knowledge, specialist engines) keeps
        the normal flow.
        """
        if not self.gate_course_content:
            return await super().execute(context)

        query = context.metadata.get("query", "")
        enrolled_slugs = await self._resolve_enrolled_slugs(context)

        # 1. If the query names a specific catalog course, gate on it directly
        # (the retriever is scoped to enrolled courses, so it can never surface
        # a not-enrolled course on its own).
        named_course = self._resolve_named_course_slug(query)
        if named_course and named_course not in enrolled_slugs:
            return await self._execute_gated(context, query, named_course)

        # 2. Otherwise fall back to the top retrieved document's course.
        documents, answer_source = await self._retrieve(
            query, context, enrolled_slugs=enrolled_slugs
        )
        target_course = self._target_course_slug(documents)
        if target_course and target_course not in enrolled_slugs:
            return await self._execute_gated(context, query, target_course)
        return await self._complete(context, query, documents, answer_source)

    @staticmethod
    def _target_course_slug(documents):
        """Course of the top-ranked lesson-content document, if any."""
        for doc in documents:
            meta = _document_metadata(doc)
            if meta.get("source") == "lesson_content" and meta.get("course_slug"):
                return meta["course_slug"]
        return None

    @classmethod
    def _resolve_named_course_slug(cls, query: str):
        """Resolve a course explicitly named in the query, if any.

        The retriever is scoped to the learner's enrolled courses, so a query
        about a not-enrolled course must be detected directly against the
        public catalog (titles + slugs). Returns the best-matching course slug
        when a course is clearly named; ``None`` for general-knowledge queries.
        """
        import re
        from app.chat.intent.catalog_vocabulary import _tokens

        query_lower = query.lower()
        q_tokens = set(_tokens(query_lower))
        if not q_tokens:
            return None

        def _has(q_lower: str, token: str) -> bool:
            if re.search(rf"\b{re.escape(token)}\b", q_lower):
                return True
            if not token.endswith(("s", "es", "ies")):
                if re.search(rf"\b{re.escape(token)}s\b", q_lower):
                    return True
            return False

        best_slug, best_score = None, 0
        second_score = 0
        for slug, meta in load_course_catalog().items():
            if not isinstance(meta, dict):
                continue
            title_tokens = set(_tokens(str(meta.get("title") or "")))
            slug_tokens = {t for t in _tokens(slug.replace("-", " "))}
            signature = title_tokens | slug_tokens
            if not signature:
                continue
            score = sum(1 for t in signature if _has(query_lower, t))
            if score > best_score:
                second_score = best_score
                best_slug, best_score = slug, score
            elif score == best_score and score > 0:
                second_score = score
        if best_score >= 2 or (best_score == 1 and second_score == 0):
            return best_slug
        return None

    def _build_gated_course_source(self, course_slug: str) -> dict:
        """CourseSourceCard-shaped payload for the recommended course.

        Uses only public catalog metadata (title, difficulty, duration,
        description, lesson titles) — never lesson bodies.
        """
        meta = load_course_catalog().get(course_slug, {})
        level_raw = str(meta.get("difficulty", "") or "")
        level = _LEVEL_LABELS.get(level_raw.lower(), level_raw.title() if level_raw else "Beginner")

        lessons = []
        for module in meta.get("modules", []):
            for lesson in module.get("lessons", []):
                lid = lesson.get("id")
                ltitle = lesson.get("title")
                if lid and ltitle:
                    lessons.append({
                        "id": str(lid),
                        "title": ltitle,
                        "module": module.get("title", ""),
                    })
                if len(lessons) >= 4:
                    break
            if len(lessons) >= 4:
                break

        return {
            "course_id": meta.get("id") or course_slug,
            "course_slug": course_slug,
            "title": meta.get("title") or course_slug,
            "label": "Recommended Course",
            "rank": 1,
            "lessons": lessons,
            "lessons_count": len(lessons),
            "progress": None,
            "duration": str(meta.get("duration") or "N/A"),
            "level": level,
            "description": meta.get("description") or "",
            "thumbnail": None,
            "rating": None,
            "action": {"label": "View Course", "url": f"/courses/{course_slug}"},
            "course_action": {"label": "View Course", "url": f"/courses/{course_slug}"},
        }

    async def _execute_gated(self, context: ExecutionContext, query: str, course_slug: str):
        """Short overview + recommendation card for a course the learner is not
        enrolled in. The LLM never receives the course's lesson content — only
        the public catalog metadata used for the recommendation card."""
        course_source = self._build_gated_course_source(course_slug)
        persona = _GATED_OVERVIEW_PERSONA(course_source.get("title") or course_slug)

        metadata = {
            "agent": self.agent_id,
            "engine": self.name,
            "sources": [],
            "llm_used": True,
            "recommendation_used": True,
            "content_gated": True,
            "gated_course_slug": course_slug,
            "course_sources": [course_source],
            "repositories": [],
            "intent": context.metadata.get("intent", ""),
            "domain": context.metadata.get("domain", ""),
            "answer_source": "gated",
        }

        enhanced_context = {
            **context.memory,
            "agent_persona": persona,
            "answer_source": "gated",
            "gated_course": course_source,
            "course_pointer": "",
        }
        prompt, system_prompt = self._prompt_builder.build_prompt(query, enhanced_context)

        from app.prompt_builder.simple_prompt_builder import RESPONSE_STYLE_BLOCK
        combined_system = f"{system_prompt}\n\n{persona}\n\n{RESPONSE_STYLE_BLOCK}"

        images = context.metadata.get("images")
        if context.streaming_mode:
            generator = self._llm.stream(prompt, system_prompt=combined_system, images=images)
            return ExecutionResult.success(
                engine=self.name,
                message="[Streaming Generator]",
                metadata={"generator": generator, **metadata},
                documents=[],
                citations=[],
            )

        response = await self._llm.generate(prompt, system_prompt=combined_system, images=images)
        return ExecutionResult.success(
            engine=self.name,
            message=response,
            metadata=metadata,
            documents=[],
            citations=[],
        )


def _GATED_OVERVIEW_PERSONA(course_title: str) -> str:
    """Persona for a not-enrolled content request: short overview only.

    Instructs the LLM to give a concise overview + why it matters and to
    recommend the BlueTeamers course — and never to reproduce full notes,
    cheat sheets, revision material, or detailed lesson content.
    """
    return (
        "You are the BlueTeamers AI Learning Coach — an experienced SOC analyst "
        "and cybersecurity instructor. The learner asked for study content (notes, "
        "a summary, a cheat sheet, or revision material) about a topic that is "
        "covered by a BlueTeamers course they are not yet enrolled in.\n"
        "Give them a SHORT overview only:\n"
        "## Overview\n"
        "2-4 concise paragraphs explaining the topic and how it relates to SOC / "
        "blue team work.\n"
        "## Why It Matters\n"
        "A short paragraph on why this topic matters for a cybersecurity career.\n"
        "Rules:\n"
        "- Do NOT generate full study notes, cheat sheets, revision material, "
        "lesson summaries, or detailed course content. The detailed material "
        "lives inside the BlueTeamers course.\n"
        "- Do not fabricate course content you cannot see; base the overview on "
        "general cybersecurity knowledge.\n"
        "- End by recommending the BlueTeamers course: "
        f"'{course_title}'. Invite the learner to enroll to unlock the full "
        "structured lessons and hands-on labs.\n"
        "- Reply in plain Markdown text only; do not generate any interactive UI."
    )


NOTES_PERSONA = (
    "You are the BlueTeamers AI Notes Generator — an experienced SOC analyst "
    "and cybersecurity instructor. The learner asked you to generate study "
    "notes (or a revision guide, cheat sheet, or quick notes).\n"
    "Produce well-structured Markdown notes with EXACTLY these sections:\n"
    "# <Topic>\n"
    "## Overview\n"
    "## Key Concepts\n"
    "## Important Commands\n"
    "## Important Event IDs\n"
    "## MITRE ATT&CK Mapping (if applicable)\n"
    "## Best Practices\n"
    "## Common Mistakes\n"
    "## Interview Tips\n"
    "## Key Takeaways\n"
    "Rules:\n"
    "- Base every section strictly on the [Context] documents (the learner's "
    "course material) or your general cybersecurity knowledge when no context "
    "is provided.\n"
    "- Keep notes concise, bullet-based, and easy to revise — no long "
    "paragraphs.\n"
    "- If a section has nothing to include (e.g. no Event IDs), write 'None' "
    "rather than inventing content.\n"
    "- Tailor depth to the learner's level in the [Persona] block.\n"
    "- Reply in plain Markdown text only; do not generate any interactive UI."
)


class NotesGenerationEngine(CourseFirstAgentEngine):
    agent_id = "notes_generator"
    persona = NOTES_PERSONA
    top_k = 8
    gate_course_content = True


TOPIC_SUMMARY_PERSONA = (
    "You are the BlueTeamers AI Learning Coach — an experienced SOC analyst "
    "and cybersecurity instructor. The learner asked for a short summary of a "
    "topic, a quick revision, or a TL;DR.\n"
    "Produce a concise, well-structured Markdown summary with EXACTLY these "
    "sections:\n"
    "## Overview\n"
    "## Key Points\n"
    "## Important Concepts\n"
    "## Real-world Importance\n"
    "## Best Practices\n"
    "## Related Topics\n"
    "Rules:\n"
    "- Base every section on the [Context] documents (course material) or your "
    "general cybersecurity knowledge when no context is provided.\n"
    "- Keep it short and scannable: use bullet points, not paragraphs.\n"
    "- If a section has nothing to include, write 'None' rather than "
    "inventing content.\n"
    "- Tailor language depth to the learner's level in the [Persona] block.\n"
    "- Reply in plain Markdown text only; do not generate any interactive UI."
)


class TopicSummaryEngine(CourseFirstAgentEngine):
    agent_id = "topic_summarizer"
    persona = TOPIC_SUMMARY_PERSONA
    top_k = 6
    gate_course_content = True
