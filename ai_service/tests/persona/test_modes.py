import pytest

from app.persona.modes import (
    ResponseMode,
    detect_mode,
    instruction_for,
)


class TestDetectMode:
    def test_default(self):
        assert detect_mode("What is a SIEM?") == ResponseMode.DEFAULT
        assert detect_mode("") == ResponseMode.DEFAULT
        assert detect_mode(None) == ResponseMode.DEFAULT

    @pytest.mark.parametrize(
        "query",
        [
            "Summarize this lesson",
            "summarise today's topic",
            "Give me revision notes",
            "What are the key takeaways?",
            "Explain in short",
            "Give me a quick summary of phishing",
            "Recap the SIEM lesson",
            "Short notes on incident response",
        ],
    )
    def test_summary_queries(self, query):
        assert detect_mode(query) == ResponseMode.SUMMARY

    @pytest.mark.parametrize(
        "query",
        [
            "Explain like I'm 5",
            "ELI5 what is a firewall",
            "Explain simply how DNS works",
            "Simplify this concept",
            "Explain in easy words",
            "Explain in simple terms",
            "Dumb it down for me",
        ],
    )
    def test_eli5_queries(self, query):
        assert detect_mode(query) == ResponseMode.ELI5

    def test_eli5_wins_over_summary(self):
        # ELI5 takes precedence when both markers are present.
        assert detect_mode("Explain simply and summarize") == ResponseMode.ELI5


class TestInstructionFor:
    def test_summary_block(self):
        block = instruction_for(ResponseMode.SUMMARY)
        assert "Structured Summary" in block
        assert "## Overview" in block
        assert "## Key Concepts" in block
        assert "## Important Commands" in block
        assert "## Important Event IDs" in block
        assert "## Best Practices" in block
        assert "## Interview Tips" in block
        assert "## Key Takeaways" in block

    def test_eli5_block(self):
        block = instruction_for(ResponseMode.ELI5)
        assert "Explain Like I'm 5" in block
        assert "no jargon" in block
        assert "analogies" in block

    def test_default_returns_none(self):
        assert instruction_for(ResponseMode.DEFAULT) is None
