import pytest
from app.prompt_builder.simple_prompt_builder import SimplePromptBuilder
from app.persona.builder import PersonaPromptBuilder


@pytest.fixture
def system_prompt_builder():
    return SimplePromptBuilder()


class TestSimplePromptBuilderPersonaIntegration:
    def test_persona_block_injected(self, system_prompt_builder):
        builder = PersonaPromptBuilder()
        block = builder.build_persona_block(memory={}, metadata={})
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "hi", {"persona_block": block, "learner_level": "beginner"}
        )
        assert "[Persona]" in system_prompt
        assert "[Learner Level]" in system_prompt
        assert "beginner" in system_prompt

    def test_memory_keys_injected_at_top_level(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "hi",
            {
                "recent_context": "User: hello\nAssistant: hi",
                "platform_context": "### User Platform Context ###\nName: Bob",
            },
        )
        assert "[Conversation History]" in system_prompt
        assert "[User Platform Context]" in system_prompt
        assert "Name: Bob" in system_prompt

    def test_nested_memory_keys_still_supported(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "hi",
            {
                "memory": {
                    "recent_context": "User: hello\nAssistant: hi",
                    "platform_context": "### User Platform Context ###\nName: Bob",
                }
            },
        )
        assert "[Conversation History]" in system_prompt
        assert "[User Platform Context]" in system_prompt

    def test_no_persona_when_absent(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt("hi", {})
        assert "[Personality]" not in system_prompt
        assert "TARGET LEVEL" not in system_prompt

    def test_ambiguous_terms_default_to_cybersecurity(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt("siem", {})
        assert "ALWAYS interpreted in their cybersecurity meaning" in system_prompt
        assert "never ask" in system_prompt

    def test_persona_domain_priority_defaults_to_cybersecurity(self):
        from app.persona.personas import CYBERSECURITY_MENTOR_PERSONA

        assert "ALWAYS interpreted in their cybersecurity meaning" in (
            CYBERSECURITY_MENTOR_PERSONA.domain_priority
        )

    def test_summary_mode_block_injected(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "Summarize this lesson", {}
        )
        assert "[Response Mode: Structured Summary]" in system_prompt
        assert "## Overview" in system_prompt

    def test_eli5_mode_block_injected(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "Explain like I'm 5 what is a firewall", {}
        )
        assert "[Response Mode: Explain Like I'm 5]" in system_prompt
        assert "no jargon" in system_prompt

    def test_eli5_overrides_summary_mode(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "Explain simply and summarize the topic", {}
        )
        assert "[Response Mode: Explain Like I'm 5]" in system_prompt
        assert "Structured Summary" not in system_prompt

    def test_default_mode_has_no_mode_block(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "What is a SIEM?", {}
        )
        assert "[Response Mode:" not in system_prompt

    def test_course_source_labeling_rule(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "What is phishing?",
            {
                "retrieved_documents": [
                    {
                        "content": "Phishing lesson text",
                        "metadata": {"course_title": "SOC 101", "lesson_title": "L1"},
                    }
                ]
            },
        )
        assert "From your course material:" in system_prompt
        assert "general knowledge" in system_prompt

    def test_course_source_recommendation_rule(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "What is phishing?",
            {
                "retrieved_documents": [
                    {
                        "content": "Phishing lesson text",
                        "metadata": {"course_title": "SOC 101", "lesson_title": "L1"},
                    }
                ],
                "answer_source": "course",
                "course_pointer": "Covered in Module 'Phishing' of SOC 101 (Lesson: L1)",
            },
        )
        assert "From your course material:" in system_prompt
        assert "Covered in Module 'Phishing'" in system_prompt

    def test_general_knowledge_source_rule(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "What is DNS?",
            {
                "retrieved_documents": [
                    {
                        "content": "DNS info",
                        "metadata": {"course_title": "", "lesson_title": ""},
                    }
                ],
                "answer_source": "general",
            },
        )
        assert "From our general knowledge base:" in system_prompt
        assert "did not match the user's course material" in system_prompt

    def test_external_tool_results_block_injected(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "Explain CVE-2024-1234",
            {
                "external_fallback": True,
                "external_tool_results": [
                    {"tool": "IndicatorFetcherTool", "input": {"indicator": "CVE-2024-1234"},
                     "output": {"malicious": True, "reputation_score": 5}},
                ],
            },
        )
        assert "[External Tool Results]" in system_prompt
        assert "IndicatorFetcherTool" in system_prompt
        assert "reputation_score" in system_prompt

    def test_external_tool_results_no_data_message(self, system_prompt_builder):
        prompt, system_prompt = system_prompt_builder.build_prompt(
            "Explain CVE-2024-1234",
            {"external_fallback": True, "external_tool_results": []},
        )
        assert "[External Tool Results]" in system_prompt
        assert "No external threat-intelligence tool returned data" in system_prompt
