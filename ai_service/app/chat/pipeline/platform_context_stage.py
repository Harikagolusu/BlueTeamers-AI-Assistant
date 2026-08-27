import re
from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.platform.context.user_context import UserContextBuilder
from app.chat.intent.models.intent_types import IntentType

# Deterministic platform relevance check (zero LLM cost)
_PLATFORM_RELEVANT_KEYWORDS = (
    "what courses", "my courses", "enrolled", "enrollment", "progress",
    "which course", "next course", "continue", "recommend", "certificate",
    "account", "profile", "dashboard", "my progress", "course progress",
    "which course should", "what should i learn", "learning path",
)
_EXCLUSION_PHRASES = (
    "do not mention my courses", "do not mention my progress", "do not mention my account",
    "do not include my courses", "do not include my progress", "do not include personal",
    "do not display my course", "do not access my course", "do not mention.*personal",
    "do not access or display my course", "do not access.*course data", "do not display.*course data",
)
_TRANSLATION_ONLY_PHRASES = (
    "translation only", "translate only", "only translate", "do not add any other information",
)


def _is_platform_relevant(query: str, intent) -> bool:
    if intent in {
        IntentType.PLATFORM_COURSE, IntentType.PLATFORM_PROGRESS,
        IntentType.PLATFORM_CERTIFICATE, IntentType.PLATFORM_ASSESSMENT,
        IntentType.PLATFORM_PROFILE, IntentType.PLATFORM_DASHBOARD,
        IntentType.PLATFORM_BADGE, IntentType.PLATFORM_LEARNING_PATH,
        IntentType.PLATFORM_LAB,
    }:
        return True
    q = (query or "").lower()
    return any(kw in q for kw in _PLATFORM_RELEVANT_KEYWORDS)


def _has_exclusion(query: str) -> bool:
    q = (query or "").lower()
    # First check exact phrases
    if any(re.search(p, q) for p in _EXCLUSION_PHRASES):
        return True
    # General pattern: "do not" + (mention/display/access/include) + ... + (course/progress/account/personal)
    # Handles "Do not access or display my course data" and similar with intervening words
    if "do not" in q and any(v in q for v in ["mention", "display", "access", "include"]) and any(n in q for n in ["course", "progress", "account", "personal"]):
        # Ensure the "do not" is before the personal noun
        do_not_idx = q.find("do not")
        # Find the personal noun after "do not"
        for noun in ["course", "progress", "account", "personal"]:
            if noun in q[do_not_idx:]:
                return True
    return False


def _is_translation_only(query: str) -> bool:
    q = (query or "").lower()
    return any(p in q for p in _TRANSLATION_ONLY_PHRASES)

class PlatformContextLoadStage(IExecutionStage):
    """Retrieves the user's platform context (cached) and injects it into memory."""
    
    def __init__(self, user_context_builder: UserContextBuilder):
        self._user_context_builder = user_context_builder

    @property
    def name(self) -> str:
        return "LoadPlatformContext"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        token = context.metadata.get("token")
        if not token:
            return context

        query = context.metadata.get("query", "") or ""
        # Check exclusion/translation first (highest priority)
        has_exclusion = _has_exclusion(query)
        is_translation_only = _is_translation_only(query)
        if has_exclusion or is_translation_only:
            new_memory = dict(context.memory) if context.memory else {}
            new_memory["platform_context"] = ""
            new_memory["exclude_platform"] = True
            if is_translation_only:
                new_memory["translation_only"] = True
            return context.with_memory(new_memory)

        # Check relevance - only load for platform-relevant queries
        intent = None
        analysis = context.metadata.get("intent_analysis")
        if analysis and getattr(analysis, "primary_intent", None):
            intent = analysis.primary_intent.type
        # Fallback to routing decision or direct intent
        if intent is None:
            routing = context.metadata.get("routing_decision")
            if routing and getattr(routing, "domain", None):
                # For platform domain, consider relevant
                from app.chat.routing.domains import CyberDomain
                if routing.domain == CyberDomain.PLATFORM:
                    intent = IntentType.PLATFORM_COURSE

        if not _is_platform_relevant(query, intent):
            new_memory = dict(context.memory) if context.memory else {}
            new_memory["platform_context"] = ""
            return context.with_memory(new_memory)
            
        platform_context_str = await self._user_context_builder.build(token)
        
        # Add to memory dictionary
        new_memory = dict(context.memory) if context.memory else {}
        new_memory["platform_context"] = platform_context_str
        
        return context.with_memory(new_memory)
