from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.llm.interfaces import ILLMService
from app.prompt_builder.interfaces import IPromptBuilder
from app.persona.greeting import GreetingResponseBuilder
from app.persona.off_topic import OffTopicResponseBuilder


class GeneralExecutionEngine(IExecutionEngine):
    """
    General engine for standard conversational queries.
    Utilizes DI for LLM and Prompt construction.
    """
    def __init__(self, llm_service: ILLMService, prompt_builder: IPromptBuilder):
        self._llm = llm_service
        self._prompt_builder = prompt_builder
        self._greeting_builder = GreetingResponseBuilder()
        self._off_topic_builder = OffTopicResponseBuilder()

    @property
    def name(self) -> str:
        return "GENERAL"

    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        query = context.metadata.get("query", "")
        intent = context.metadata.get("intent", "")

        metadata = {
            "agent": "general_assistant",
            "engine": self.name,
            "sources": [],
            "llm_used": True,
            "recommendation_used": False,
            "repositories": [],
            "intent": intent,
            "domain": context.metadata.get("domain", ""),
        }

        # 0. Templated responses: greetings and small talk are answered with a
        # persona-aware template so no LLM tokens are spent on trivial queries.
        # The greeting / off-topic templates are English-only, so for any
        # non-English response language they are skipped and the LLM answers
        # with the [Response Language] block in the correct language instead.
        language = (context.memory or {}).get("language") or "en"
        use_english_templates = language in ("en", "auto", None)
        if use_english_templates and self._greeting_builder.supports(query, intent):
            message = self._greeting_builder.build(
                query, intent, memory=context.memory, metadata=context.metadata
            )
            metadata = {**metadata, "llm_used": False}
            return ExecutionResult.success(engine=self.name, message=message, metadata=metadata)

        # 0b. Off-topic refusal: the assistant only answers cybersecurity
        # content. Out-of-scope queries are refused with a template (no LLM).
        if use_english_templates and self._off_topic_builder.supports(query, intent):
            message = self._off_topic_builder.build(
                query, intent, memory=context.memory, metadata=context.metadata
            )
            metadata = {**metadata, "llm_used": False}
            return ExecutionResult.success(engine=self.name, message=message, metadata=metadata)

        # 1. Prompt Building
        prompt, system_prompt = self._prompt_builder.build_prompt(query, context.memory)

        # 2. LLM Execution (Streaming vs Non-Streaming)
        images = context.metadata.get("images")
        if context.streaming_mode:
            # We wrap the generator into a placeholder execution result which
            # CompositionStage handles.
            generator = self._llm.stream(
                prompt, system_prompt=system_prompt, images=images
            )
            return ExecutionResult.success(
                engine=self.name,
                message="[Streaming Generator]",
                metadata={"generator": generator, **metadata}
            )
        else:
            response = await self._llm.generate(
                prompt, system_prompt=system_prompt, images=images
            )
            return ExecutionResult.success(
                engine=self.name,
                message=response,
                metadata=metadata
            )
