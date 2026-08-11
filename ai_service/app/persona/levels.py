"""Learner proficiency levels and their teaching guidance.

Each level carries a `teaching_guidance` block that the persona prompt builder
injects into the system prompt so every response is tailored to the learner's
current level without the user having to specify it.
"""
from dataclasses import dataclass
from enum import Enum


class LearnerLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"
    INSTRUCTOR = "instructor"


@dataclass(frozen=True)
class LevelProfile:
    label: str
    teaching_guidance: str


LEVEL_PROFILES: dict[LearnerLevel, LevelProfile] = {
    LearnerLevel.BEGINNER: LevelProfile(
        label="Beginner",
        teaching_guidance=(
            "TARGET LEVEL: Beginner.\n"
            "- Explain everything simply; avoid unnecessary jargon.\n"
            "- When you must use a technical term, define it in plain language right away.\n"
            "- Use analogies and concrete real-world examples to anchor each concept.\n"
            "- Explain WHY the concept matters before diving into HOW it works.\n"
            "- Keep each explanation focused; one idea at a time.\n"
            "- Encourage the learner: acknowledge progress and keep the tone supportive."
        ),
    ),
    LearnerLevel.INTERMEDIATE: LevelProfile(
        label="Intermediate",
        teaching_guidance=(
            "TARGET LEVEL: Intermediate.\n"
            "- Assume the learner knows the fundamentals; avoid re-explaining basics.\n"
            "- Introduce industry terminology and use it naturally (SIEM, IOC, TTP, correlation, etc.).\n"
            "- Explain workflows and connect concepts together rather than isolated facts.\n"
            "- Show how detection and analysis steps chain into a complete investigation.\n"
            "- Keep explanations tight but complete; add brief real-world context when useful."
        ),
    ),
    LearnerLevel.ADVANCED: LevelProfile(
        label="Advanced",
        teaching_guidance=(
            "TARGET LEVEL: Advanced.\n"
            "- Assume a strong grasp of cybersecurity fundamentals.\n"
            "- Focus on detection logic, MITRE ATT&CK mapping, investigation depth, and best practices.\n"
            "- Discuss trade-offs explicitly (e.g., coverage vs. false positives, cost vs. fidelity).\n"
            "- Prefer real-world scenarios, log snippets, and detection snippets over generic theory.\n"
            "- Challenge the learner with follow-up questions that exercise analytical reasoning."
        ),
    ),
    LearnerLevel.PROFESSIONAL: LevelProfile(
        label="Professional",
        teaching_guidance=(
            "TARGET LEVEL: Professional (senior SOC analyst).\n"
            "- Discuss detection engineering, threat hunting, performance, and architecture.\n"
            "- Address enterprise deployment concerns: scale, tuning, false-positive management.\n"
            "- Reference operational considerations (alert lifecycle, case management, runbooks).\n"
            "- Give opinions grounded in evidence and weigh engineering trade-offs.\n"
            "- Expect and encourage precise, production-ready language."
        ),
    ),
    LearnerLevel.INSTRUCTOR: LevelProfile(
        label="Instructor",
        teaching_guidance=(
            "TARGET LEVEL: Instructor.\n"
            "- Support generating teaching material: lesson plans, slides outlines, quiz questions.\n"
            "- Produce interview questions, practice exercises, assessments, labs, and learning paths.\n"
            "- Provide answer keys and grading rubrics where appropriate.\n"
            "- Structure material for classroom or self-paced delivery.\n"
            "- Help the user build effective teaching content for others."
        ),
    ),
}


def get_level(level: str | LearnerLevel | None) -> LearnerLevel:
    if isinstance(level, LearnerLevel):
        return level
    if not level:
        return LearnerLevel.BEGINNER
    try:
        return LearnerLevel(level.lower())
    except ValueError:
        return LearnerLevel.BEGINNER
