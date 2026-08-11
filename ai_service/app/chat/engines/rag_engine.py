from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.rag.interfaces import IRetriever
from app.llm.interfaces import ILLMService
from app.prompt_builder.interfaces import IPromptBuilder
from app.chat.engines.citations import build_citations
from app.chat.engines.course_sources import build_course_sources, build_course_pointer

import logging

logger = logging.getLogger("app.chat.engines.rag_engine")

class RagExecutionEngine(IExecutionEngine):
    """
    Executes informational queries by retrieving domain-specific documents
    and synthesizing a response.
    """
    def __init__(
        self,
        retriever: IRetriever,
        llm_service: ILLMService,
        prompt_builder: IPromptBuilder,
        platform_repo=None,
    ):
        self._retriever = retriever
        self._llm = llm_service
        self._prompt_builder = prompt_builder
        self._platform_repo = platform_repo

    @property
    def name(self) -> str:
        return "RAG"

    async def _resolve_enrolled_slugs(self, context: ExecutionContext) -> set:
        """
        Best-effort: for authenticated users, resolves the slugs of courses the
        learner is enrolled in, so course content can be prioritized. Never raises.
        """
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

    async def _resolve_progress(self, context: ExecutionContext, course_slugs: set) -> dict:
        """
        Best-effort: for authenticated users, look up per-course completion
        percentages so Course Source Cards can show progress. Never raises.
        """
        if not self._platform_repo or not course_slugs:
            return {}
        token = context.metadata.get("token")
        if not token:
            return {}
        progress = {}
        try:
            enrolled = await self._platform_repo.get_enrolled_courses(token)
            enrolled_slugs = {c.id for c in enrolled}
            for slug in course_slugs:
                if slug in enrolled_slugs:
                    try:
                        p = await self._platform_repo.get_progress(slug, token)
                    except Exception:
                        p = None
                    if p:
                        progress[slug] = p.percent_complete
        except Exception as e:
            logger.warning(f"Course-source progress resolution failed: {e}")
        return progress

    async def _retrieve_course_first(
        self, query: str, enrolled_slugs: set, top_k: int = 5
    ):
        """
        Course-material-first retrieval: when the learner is enrolled in
        courses, search their lesson content first. Returns
        (documents, answer_source) where answer_source is "course" or "general".
        """
        if not enrolled_slugs:
            return await self._retriever.search(query, top_k=top_k), "general"

        course_docs = await self._retriever.search(
            query,
            top_k=top_k,
            metadata_filters={
                "source": "lesson_content",
                "course_slug": list(enrolled_slugs),
            },
        )
        if course_docs:
            return course_docs, "course"

        # Fall back to the general knowledge base when course material has no match.
        return await self._retriever.search(query, top_k=top_k), "general"

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        query = context.metadata.get("query", "")

        # 1. Course-first retrieval: prioritize the learner's enrolled course
        # material; fall back to the general knowledge base when there is no
        # match. `answer_source` labels where the answer was grounded.
        enrolled_slugs = await self._resolve_enrolled_slugs(context)
        documents, answer_source = await self._retrieve_course_first(query, enrolled_slugs)

        # Format documents for context
        doc_contexts = [{"content": d.content, "metadata": d.metadata} for d in documents]

        # Structured metadata: agent is the single selected agent for this request.
        decision = context.metadata.get("routing_decision")
        agent_id = getattr(decision, "agent_id", "knowledge_assistant") if decision else "knowledge_assistant"
        metadata = {
            "agent": agent_id,
            "engine": self.name,
            "sources": doc_contexts,
            "llm_used": True,
            "recommendation_used": False,
            "repositories": [],
            "intent": context.metadata.get("intent", ""),
            "domain": context.metadata.get("domain", ""),
            "answer_source": answer_source,
        }

        # Course Source Cards: emit automatically whenever the answer is
        # grounded in BlueTeamers lesson chunks.
        lesson_slugs = {
            d.metadata.get("course_slug")
            for d in documents
            if (d.metadata or {}).get("source") == "lesson_content" and d.metadata.get("course_slug")
        }
        progress_by_slug = await self._resolve_progress(context, lesson_slugs)
        course_sources = build_course_sources(documents, progress_by_slug=progress_by_slug or None)
        metadata["course_sources"] = course_sources

        # Course pointer: a short, user-facing recommendation of the lesson /
        # module that covers the answer, so the text response can recommend the
        # relevant material (e.g. "This topic is covered in Module 4: Windows
        # Event Logs."). Derived from the top course source card.
        course_pointer = build_course_pointer(course_sources)

        # When nothing was retrieved, decide between two honest behaviours:
        #   - Course-content query  -> admit the material isn't in the knowledge base, ask which lesson
        #   - General-knowledge query (e.g. "what is Python?") -> fall back to a plain LLM answer
        is_course_query = any(kw in query.lower() for kw in
                              ["module", "lesson", "section", "chapter", "concept",
                               "course", "understand", "doubt", "topic"])
        empty_retrieval = len(documents) == 0 and is_course_query

        # 2. Prompt Building
        enhanced_context = {
            **context.memory,
            "retrieved_documents": doc_contexts,
            "empty_retrieval": empty_retrieval,
            "answer_source": answer_source,
            "course_pointer": course_pointer,
        }
        prompt, system_prompt = self._prompt_builder.build_prompt(query, enhanced_context)

        # 3. LLM Execution
        images = context.metadata.get("images")
        if context.streaming_mode:
            generator = self._llm.stream(
                prompt, system_prompt=system_prompt, images=images
            )
            return ExecutionResult.success(
                engine=self.name,
                message="[Streaming Generator]",
                metadata={"generator": generator, **metadata},
                documents=doc_contexts,
                citations=build_citations(documents)
            )
        else:
            response = await self._llm.generate(
                prompt, system_prompt=system_prompt, images=images
            )
            return ExecutionResult.success(
                engine=self.name,
                message=response,
                metadata=metadata,
                documents=doc_contexts,
                citations=build_citations(documents)
            )

