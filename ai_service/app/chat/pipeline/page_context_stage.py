"""Page-context injection stage (Sprint 5, Feature 5 — Context Awareness).

The frontend floating assistant automatically detects where the learner is
(Dashboard, Course, Lesson, Practice Lab, Wazuh Lab, Profile, ...) and sends
that structured payload as ``request.context.page``. This stage reads it and
injects a ``page_context`` block into the conversation memory so every engine's
prompt builder can render "[Page Context]" into the system prompt.

The AI therefore already knows "which lesson is open" or "which Wazuh lab is
active" without the user having to explain where they are.
"""
import logging
from typing import Any, Dict, Optional

from app.chat.context.execution_context import ExecutionContext
from app.chat.interfaces.i_execution_stage import IExecutionStage

logger = logging.getLogger("app.chat.pipeline.page_context_stage")

# Human-readable labels for the page types the frontend reports.
_PAGE_LABELS: Dict[str, str] = {
    "dashboard": "Dashboard",
    "course": "Course page",
    "lesson": "Lesson",
    "quiz": "Quiz",
    "lab": "Practice Lab",
    "wazuh": "Wazuh Lab",
    "threat_intel": "Threat Intelligence",
    "email_security": "Email Security Lab",
    "profile": "Profile",
    "settings": "Settings",
    "alerts": "Alerts",
    "incidents": "Incidents",
    "endpoints": "Endpoints",
    "logs": "Lab Logs",
    "workspace": "AI Workspace",
}


def build_page_context_block(page: Dict[str, Any]) -> str:
    """Compile the page payload into a concise prompt block."""
    if not isinstance(page, dict) or not page.get("type"):
        return ""
    page_type = str(page.get("type", "")).lower()
    label = _PAGE_LABELS.get(page_type, page_type.replace("_", " ").title())
    parts: list = [f"[Page Context]\nThe learner is currently on: {label}."]

    course_title = page.get("course_title") or page.get("course") or ""
    lesson_title = page.get("lesson_title") or page.get("lesson") or ""
    lab_title = page.get("lab_title") or page.get("lab") or ""
    alert_id = page.get("alert_id")
    path = page.get("path") or ""

    if lesson_title:
        parts.append(f"Active lesson: {lesson_title}" + (f" (course: {course_title})" if course_title else ""))
    elif course_title:
        parts.append(f"Active course: {course_title}")
    if lab_title:
        parts.append(f"Active lab: {lab_title}" + (f" ({alert_id})" if alert_id else ""))
    if path:
        parts.append(f"Page path: {path}")

    parts.append(
        "Use this context to answer the learner's question about what they are "
        "currently viewing. Do not ask them where they are; infer it from this block."
    )
    return "\n".join(parts)


class PageContextStage(IExecutionStage):
    """Injects the frontend-reported page context into conversation memory."""

    @property
    def name(self) -> str:
        return "PageContextStage"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        req_context = context.metadata.get("context")
        page: Optional[Dict[str, Any]] = None
        if isinstance(req_context, dict):
            candidate = req_context.get("page")
            if isinstance(candidate, dict):
                page = candidate
        if not page:
            return context

        block = build_page_context_block(page)
        if not block:
            return context

        new_memory = dict(context.memory) if context.memory else {}
        new_memory["page_context"] = block
        return context.with_memory(new_memory)
