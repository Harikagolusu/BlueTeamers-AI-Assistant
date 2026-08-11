"""Response mode detection for the BlueTeamers AI Workspace.

Two special response modes adjust only the current response (they are detected
per-query, never persisted):

  - SUMMARY: "summarize this lesson", "revision notes", "key takeaways" ->
    the AI produces a structured summary (overview, key concepts, commands,
    event IDs, best practices, interview tips, takeaways).

  - ELI5: "explain like I'm 5", "explain simply" -> an extremely beginner-
    friendly, jargon-free explanation with analogies.

Both are detected from the raw query text by the ResponseModeDetector and the
matching instruction block is injected by SimplePromptBuilder.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ResponseMode(str, Enum):
    DEFAULT = "default"
    SUMMARY = "summary"
    ELI5 = "eli5"


_SUMMARY_MARKERS = (
    "summarize",
    "summarise",
    "summary",
    "revision notes",
    "revision points",
    "key takeaways",
    "key points",
    "takeaways",
    "explain in short",
    "in short",
    "short notes",
    "brief summary",
    "quick summary",
    "recap",
    "overview of the lesson",
    "sum it up",
    "gist",
)

_ELI5_MARKERS = (
    "explain like i'm 5",
    "explain like i am 5",
    "explain like i'm five",
    "eli5",
    "explain simply",
    "explain in simple terms",
    "explain in easy words",
    "simplify this",
    "simplify it",
    "simplify",
    "in simple words",
    "dumb it down",
    "explain in layman",
    "for a child",
)


def detect_mode(query: Optional[str]) -> ResponseMode:
    """Returns SUMMARY / ELI5 when the query requests one, else DEFAULT.

    ELI5 takes precedence when both are present so simplification wins.
    """
    if not query:
        return ResponseMode.DEFAULT
    lowered = query.strip().lower()
    if any(marker in lowered for marker in _ELI5_MARKERS):
        return ResponseMode.ELI5
    if any(marker in lowered for marker in _SUMMARY_MARKERS):
        return ResponseMode.SUMMARY
    return ResponseMode.DEFAULT


@dataclass(frozen=True)
class ModeInstruction:
    label: str
    block: str


_SUMMARY_INSTRUCTION = ModeInstruction(
    label="summary",
    block=(
        "[Response Mode: Structured Summary]\n"
        "The user asked for a summary, revision notes, or key takeaways. "
        "Produce a concise, well-structured summary with these exact sections "
        "using markdown headings:\n"
        "## Overview\n"
        "## Key Concepts\n"
        "## Important Commands\n"
        "## Important Event IDs\n"
        "## Best Practices\n"
        "## Interview Tips\n"
        "## Key Takeaways\n"
        "Rules:\n"
        "- Base every section strictly on the [Context] documents (or your "
        "general cybersecurity knowledge if no context is provided).\n"
        "- Keep it concise; use bullet points and short lines, not paragraphs.\n"
        "- If a section has nothing to include (e.g. no Event IDs), state "
        "'None' rather than inventing content.\n"
        "- Tailor language depth to the learner's level in the [Persona] block."
    ),
)

_ELI5_INSTRUCTION = ModeInstruction(
    label="eli5",
    block=(
        "[Response Mode: Explain Like I'm 5]\n"
        "The user asked for an extremely simple explanation. Override the "
        "normal level guidance for THIS response only.\n"
        "Rules:\n"
        "- Use very simple language a child could follow; no jargon.\n"
        "- When a technical term is unavoidable, define it in one plain sentence.\n"
        "- Use everyday analogies and a concrete real-life example.\n"
        "- Keep it short and friendly; one idea at a time.\n"
        "- Reassure the learner that even professionals started at this level."
    ),
)


def instruction_for(mode: ResponseMode) -> Optional[str]:
    if mode == ResponseMode.SUMMARY:
        return _SUMMARY_INSTRUCTION.block
    if mode == ResponseMode.ELI5:
        return _ELI5_INSTRUCTION.block
    return None
