import pytest

from app.persona.greeting import (
    GreetingResponseBuilder,
    _extract_courses,
    _extract_name,
)


@pytest.fixture
def builder():
    return GreetingResponseBuilder()


PLATFORM_CONTEXT = (
    "### User Platform Context ###\n"
    "Name: Ada Lovelace\n"
    "Active Enrollments: SOC Analyst Fundamentals, Threat Hunting 101\n"
    "Recent Progress: SOC Analyst Fundamentals (45% - 6 lessons completed)\n"
    "Certificates: None.\n"
)


class TestExtraction:
    def test_extracts_name(self):
        assert _extract_name(PLATFORM_CONTEXT) == "Ada Lovelace"

    def test_extracts_courses(self):
        assert _extract_courses(PLATFORM_CONTEXT) == (
            "SOC Analyst Fundamentals, Threat Hunting 101"
        )

    def test_missing_context(self):
        assert _extract_name(None) is None
        assert _extract_courses(None) is None

    def test_unavailable_values(self):
        ctx = "Name: Not available.\nActive Enrollments: None."
        assert _extract_name(ctx) is None
        assert _extract_courses(ctx) is None


class TestGreetingBuilder:
    def test_supports_greeting(self):
        assert GreetingResponseBuilder.supports("hi", "GREETING")

    def test_supports_small_talk(self):
        assert GreetingResponseBuilder.supports("how are you", "SMALL_TALK")

    def test_does_not_support_rag(self):
        assert not GreetingResponseBuilder.supports("what is siem", "RAG_CHAT")

    def test_builds_greeting_with_platform_context(self, builder):
        response = builder.build(
            "hello",
            "GREETING",
            memory={
                "learner_level": "intermediate",
                "platform_context": PLATFORM_CONTEXT,
            },
        )
        assert "Ada Lovelace" in response
        assert "BlueTeamers" in response
        assert "SOC" in response or "security operations" in response.lower()
        # Courses are displayed in the opening dashboard, so the greeting must
        # not repeat them.
        assert "SOC Analyst Fundamentals" not in response
        assert "- Threat Hunting 101" not in response
        assert "🚀" not in response and "🔹" not in response and "📚" not in response

    def test_builds_greeting_without_context(self, builder):
        response = builder.build("hi", "GREETING", memory={})
        assert "BlueTeamers" in response
        assert "security operations" in response.lower()

    def test_level_offer_reflects_level(self, builder):
        beginner = builder.build(
            "hello", "GREETING", memory={"learner_level": "beginner"}
        )
        advanced = builder.build(
            "hello", "GREETING", memory={"learner_level": "advanced"}
        )
        assert "fundamentals" in beginner.lower()
        assert "detection engineering" in advanced.lower()
        assert not beginner.startswith("**")
        assert "## " not in beginner

    def test_small_talk(self, builder):
        response = builder.build("thanks", "SMALL_TALK", memory={})
        assert "Happy to chat!" in response
