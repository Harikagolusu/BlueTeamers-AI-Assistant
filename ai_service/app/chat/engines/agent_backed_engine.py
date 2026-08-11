"""Base engine for specialist agents (Learning Coach, Threat Intelligence,
Investigation, Lab Mentor, Assessment Coach).

Each specialist agent retrieves grounded BlueTeamers documents and then calls the
LLM to reason over them. Structured output is returned via ExecutionResult so the
frontend renders purely from metadata (agent, sources, citations).
"""
import logging

from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.rag.interfaces import IRetriever
from app.llm.interfaces import ILLMService
from app.prompt_builder.interfaces import IPromptBuilder
from app.chat.engines.citations import build_citations
from app.chat.engines.course_sources import build_course_sources, build_course_pointer

logger = logging.getLogger("app.chat.engines.agent_backed_engine")


class AgentBackedEngine(IExecutionEngine):
    """RAG-grounded LLM engine bound to a single specialist agent persona."""

    agent_id = "knowledge_assistant"
    persona = "You are a helpful BlueTeamers assistant."
    top_k = 5
    supports_recommendations = False

    def __init__(
        self,
        retriever: IRetriever,
        llm_service: ILLMService,
        prompt_builder: IPromptBuilder,
    ):
        self._retriever = retriever
        self._llm = llm_service
        self._prompt_builder = prompt_builder

    @property
    def name(self) -> str:
        return self.agent_id.upper()

    async def _retrieve(self, query: str, context: ExecutionContext):
        """Retrieval hook returning (documents, answer_source).

        Subclasses override this to add course-first retrieval or custom
        metadata filters. The base implementation searches the general
        knowledge base and labels the source as "general".
        """
        documents = await self._retriever.search(query, top_k=self.top_k)
        return documents, "general"

    def _persona_for(
        self,
        context: ExecutionContext,
        documents,
        answer_source: str,
    ) -> str:
        """Persona hook: subclasses swap the persona per-execution (e.g. an
        external-fallback persona when the knowledge base has no match)."""
        return self.persona

    def _context_for(
        self,
        context: ExecutionContext,
        documents,
        answer_source: str,
        doc_contexts,
        course_pointer: str,
    ) -> dict:
        """Prompt-context hook: subclasses enrich the LLM context (e.g. with
        external tool results) without duplicating the execute flow."""
        return {}

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        query = context.metadata.get("query", "")

        documents, answer_source = await self._retrieve(query, context)
        return await self._complete(context, query, documents, answer_source)

    async def _complete(
        self,
        context: ExecutionContext,
        query: str,
        documents,
        answer_source: str,
    ) -> ExecutionResult:
        """Generate the final answer from already-retrieved documents.

        Splitting ``execute`` into ``_retrieve`` + ``_complete`` lets subclasses
        (e.g. the course-access gate) reuse a single retrieval to decide whether
        full content is allowed and then finish the normal flow with the same
        documents.
        """
        doc_contexts = [{"content": d.content, "metadata": d.metadata} for d in documents]

        metadata = {
            "agent": self.agent_id,
            "engine": self.name,
            "sources": doc_contexts,
            "llm_used": True,
            "recommendation_used": False,
            "repositories": [],
            "intent": context.metadata.get("intent", ""),
            "domain": context.metadata.get("domain", ""),
            "answer_source": answer_source,
        }

        course_sources = build_course_sources(documents, progress_by_slug=None)
        metadata["course_sources"] = course_sources

        course_pointer = build_course_pointer(course_sources)

        persona = self._persona_for(context, documents, answer_source)
        context_overrides = self._context_for(
            context, documents, answer_source, doc_contexts, course_pointer
        )

        enhanced_context = {
            **context.memory,
            "retrieved_documents": doc_contexts,
            "agent_persona": persona,
            "answer_source": answer_source,
            "course_pointer": course_pointer,
            **context_overrides,
        }
        prompt, system_prompt = self._prompt_builder.build_prompt(query, enhanced_context)
        # The specialist persona defines the agent's expertise and section layout.
        # The response-style block is re-appended AFTER the persona so conciseness,
        # progressive disclosure, clean-markdown and no-internal-tags rules keep
        # winning over long-form section dumps.
        from app.prompt_builder.simple_prompt_builder import RESPONSE_STYLE_BLOCK
        combined_system = f"{system_prompt}\n\n{persona}\n\n{RESPONSE_STYLE_BLOCK}"

        if context.streaming_mode:
            generator = self._llm.stream(
                prompt, system_prompt=combined_system, images=context.metadata.get("images")
            )
            return ExecutionResult.success(
                engine=self.name,
                message="[Streaming Generator]",
                metadata={"generator": generator, **metadata},
                documents=doc_contexts,
                citations=build_citations(documents),
            )

        response = await self._llm.generate(
            prompt, system_prompt=combined_system, images=context.metadata.get("images")
        )
        return ExecutionResult.success(
            engine=self.name,
            message=response,
            metadata=metadata,
            documents=doc_contexts,
            citations=build_citations(documents),
        )
