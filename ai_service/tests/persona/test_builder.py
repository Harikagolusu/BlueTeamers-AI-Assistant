import pytest
from app.persona.builder import PersonaPromptBuilder
from app.persona.levels import LearnerLevel
from app.persona.registry import PersonaRegistry
from app.persona.personas import CYBERSECURITY_MENTOR_PERSONA


@pytest.fixture
def builder():
    return PersonaPromptBuilder(registry=PersonaRegistry())


class TestPersonaPromptBuilder:
    def test_detect_level(self, builder):
        assert builder.detect_level(memory={}, metadata={}) == LearnerLevel.BEGINNER

    def test_build_persona_block_contains_core_sections(self, builder):
        block = builder.build_persona_block(memory={}, metadata={})
        assert "[Persona]" in block
        assert "[Expertise]" in block
        assert "[Communication Style]" in block
        assert "[Teaching Level]" in block
        assert "[Response Format]" in block
        assert "[Domain Priority]" in block
        assert "[Personality]" in block

    def test_build_persona_block_adapts_to_level(self, builder):
        advanced = builder.build_persona_block(
            memory={"platform_context": "Certificates: siem-fundamentals"},
            metadata={},
        )
        beginner = builder.build_persona_block(memory={}, metadata={})
        assert "TARGET LEVEL: Beginner" not in advanced
        assert "TARGET LEVEL: Beginner" in beginner

    def test_build_context_block_platform(self, builder):
        block = builder.build_context_block(
            memory={"platform_context": "### User Platform Context ###\nName: Bob"},
            metadata={},
        )
        assert "Name: Bob" in block

    def test_build_context_block_learning_context(self, builder):
        block = builder.build_context_block(
            memory={},
            metadata={"course": "SIEM Fundamentals", "lesson": "Log Sources"},
        )
        assert "Current course: SIEM Fundamentals" in block
        assert "Current lesson: Log Sources" in block

    def test_build_context_block_empty(self, builder):
        assert builder.build_context_block(memory={}, metadata={}) == ""

    def test_persona_has_cybersecurity_expertise(self, builder):
        assert "SOC Operations" in CYBERSECURITY_MENTOR_PERSONA.expertise
        assert "MITRE ATT&CK" in CYBERSECURITY_MENTOR_PERSONA.expertise
