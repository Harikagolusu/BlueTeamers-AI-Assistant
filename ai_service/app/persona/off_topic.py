"""Template-based off-topic refusal for the BlueTeamers AI Workspace.

The assistant only answers cybersecurity content. Queries that are clearly
outside that scope (jokes, cooking, movies, general trivia, non-security
programming, etc.) are refused with a templated, professional message so no
LLM tokens are spent and scope stays strict. Detection happens in the intent
classifier (OFF_TOPIC intent); this builder only renders the response.
"""
from typing import Optional


class OffTopicResponseBuilder:
    """Builds a templated scope-refusal message without calling the LLM."""

    @staticmethod
    def supports(query: str, intent: str) -> bool:
        return (intent or "").upper() == "OFF_TOPIC"

    def build(
        self,
        query: str,
        intent: str,
        memory: Optional[dict] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """Builds the scope-refusal response."""
        return (
            "I'm focused on helping you with cybersecurity content — threat "
            "intelligence, SOC operations, incident response, detection "
            "engineering, and the BlueTeamers courses and labs.\n\n"
            "That question is outside my scope. If you'd like, I can help you "
            "with a security concept, a lab, or a course topic instead."
        )
