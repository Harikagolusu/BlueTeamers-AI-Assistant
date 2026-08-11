import pytest
from app.persona.detector import LearnerLevelDetector
from app.persona.levels import LearnerLevel


@pytest.fixture
def detector():
    return LearnerLevelDetector()


class TestLevelDetection:
    def test_empty_returns_beginner(self, detector):
        assert detector.detect(memory={}, metadata={}) == LearnerLevel.BEGINNER

    def test_explicit_level_wins(self, detector):
        level = detector.detect(memory={}, metadata={"learner_level": "instructor"})
        assert level == LearnerLevel.INSTRUCTOR

    def test_certificates_and_advanced_course(self, detector):
        memory = {
            "platform_context": (
                "### User Platform Context ###\n"
                "Name: Alice\n"
                "Active Enrollments: Advanced SIEM Tuning\n"
                "Recent Progress: Advanced SIEM Tuning (95% - 12 lessons completed)\n"
                "Certificates: siem-fundamentals\n"
                "Badges: None.\n"
                "Learning Paths: None."
            )
        }
        level = detector.detect(memory=memory, metadata={})
        assert level in (LearnerLevel.ADVANCED, LearnerLevel.PROFESSIONAL)

    def test_beginner_vocabulary(self, detector):
        memory = {"recent_context": "User: what is siem? I'm new, i don't understand"}
        assert detector.detect(memory=memory, metadata={}) == LearnerLevel.BEGINNER

    def test_intermediate_vocabulary(self, detector):
        memory = {"recent_context": "User: how do I triage a siem alert in my soc"}
        assert detector.detect(memory=memory, metadata={}) == LearnerLevel.INTERMEDIATE

    def test_advanced_vocabulary(self, detector):
        memory = {
            "recent_context": (
                "User: can you walk me through threat hunting with sigma and yara "
                "for lateral movement detection?"
            )
        }
        assert detector.detect(memory=memory, metadata={}) == LearnerLevel.ADVANCED

    def test_instructor_vocabulary(self, detector):
        memory = {"recent_context": "User: help me design a lesson plan and interview questions"}
        assert detector.detect(memory=memory, metadata={}) == LearnerLevel.INSTRUCTOR

    def test_course_difficulty_signal(self, detector):
        level = detector.detect(memory={}, metadata={"course_level": "expert"})
        assert level in (LearnerLevel.ADVANCED, LearnerLevel.PROFESSIONAL)
