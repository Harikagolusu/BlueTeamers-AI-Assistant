"""
Static knowledge source loader for the Hybrid Knowledge Architecture.

Only STATIC content is loaded here:
  - Course descriptions / modules / lesson catalog   (course_catalog.json)
  - Full lesson markdown content                      (all_lessons.json)

Dynamic platform data (user profile, progress, enrollments, purchases,
assessments, certificates) is deliberately EXCLUDED from this module. It is
never embedded; it is served live from the Django APIs via the Platform
Repository.
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import Dict, Any, List

from app.core.config import settings

logger = logging.getLogger("app.knowledge.sources")

# Canonical slugs in all_lessons.json -> frontend display ids (where available)
_SLUG_DISPLAY_IDS = {
    "blue-team-soc-fundamentals": "soc-fundamentals",
    "log-analysis-for-beginners": "log-analysis",
    "network-fundamentals": "network-fundamentals",
    "siem-fundamentals": "siem-fundamentals",
    "incident-response-fundamentals": "incident-response",
    "soc-analyst-path": "soc-analyst-path",
    "network-security-monitoring": "network-security-monitoring",
    "detection-engineering-basics": "detection-engineering",
    "malware-analysis-fundamentals": "malware-analysis",
    "threat-hunting-fundamentals": "threat-hunting",
    "cybersecurity-frameworks": "cybersecurity-frameworks",
}

_SOURCE_LESSON_JSON = "lesson_content"
_SOURCE_COURSE_META = "course_metadata"


def content_hash(text: str) -> str:
    """Deterministic SHA-1 fingerprint of a document body (for incremental indexing)."""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def load_lesson_content() -> Dict[str, List[Dict[str, Any]]]:
    """Returns {course_slug: [lesson, ...]} for every course in all_lessons.json."""
    path = Path(settings.KNOWLEDGE_LESSON_JSON)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / "data" / "all_lessons.json"
    if not path.exists():
        logger.warning(
            f"Lesson content JSON not found at {path}. Static knowledge will be empty."
        )
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        return {}
    return data


def load_course_catalog() -> Dict[str, Dict[str, Any]]:
    """Returns {course_slug: {title, description, difficulty, modules, ...}}."""
    path = Path(settings.KNOWLEDGE_COURSE_JSON)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / "data" / "course_catalog.json"
    if not path.exists():
        logger.warning(f"Course catalog JSON not found at {path}.")
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return data if isinstance(data, dict) else {}


def _practical_exercise_to_markdown(exercise: Any) -> str:
    """
    Flattens a practicalExercise payload into clean markdown.

    Structured exercises are dicts with title/description/steps/labScenario/
    labQuestions. Only the *question* text of labQuestions is included — answers
    and hints are deliberately excluded so the RAG knowledge base never leaks
    lab solutions (Lab Mentor must guide without spoiling).
    """
    if isinstance(exercise, str):
        return exercise
    if not isinstance(exercise, dict):
        return str(exercise)

    parts: List[str] = []
    title = exercise.get("title")
    description = exercise.get("description")
    steps = exercise.get("steps")
    scenario = exercise.get("labScenario")
    questions = exercise.get("labQuestions")

    if title:
        parts.append(f"### {title}")
    if description:
        parts.append(str(description))
    if scenario:
        parts.append(f"**Lab Scenario:**\n\n{scenario}")
    if steps:
        parts.append("**Steps:**")
        if isinstance(steps, list):
            for idx, step in enumerate(steps, 1):
                parts.append(f"{idx}. {step}")
        else:
            parts.append(str(steps))
    if questions and isinstance(questions, list):
        parts.append("**Questions:**")
        for q in questions:
            if isinstance(q, dict):
                text = q.get("question") or q.get("id") or ""
            else:
                text = str(q)
            if text:
                parts.append(f"- {text}")
    return "\n\n".join(p for p in parts if p).strip()


def _resources_to_markdown(resources: Any) -> str:
    """Flattens an additionalResources payload into markdown bullets."""
    if isinstance(resources, str):
        return resources
    if isinstance(resources, list):
        lines: List[str] = []
        for item in resources:
            if isinstance(item, dict):
                title = item.get("title") or item.get("url") or ""
                url = item.get("url") or ""
                label = f"{title}" + (f" ({url})" if url else "")
                if label:
                    lines.append(f"- {label}")
            else:
                lines.append(f"- {item}")
        return "\n".join(lines)
    if isinstance(resources, dict):
        return "\n".join(f"- {k}: {v}" for k, v in resources.items())
    return str(resources)


def lesson_to_markdown(lesson: Dict[str, Any]) -> str:
    """
    Flattens a lesson payload into a single markdown document so the chunker
    preserves headings, code blocks, key takeaways and exercises.
    """
    parts: List[str] = []
    title = lesson.get("title", "")
    content = lesson.get("content", "")
    if title:
        parts.append(f"# {title}")
    if content:
        parts.append(str(content))

    takeaways = lesson.get("keyTakeaways")
    if takeaways:
        parts.append("## Key Takeaways")
        if isinstance(takeaways, list):
            for item in takeaways:
                parts.append(f"- {item}")
        else:
            parts.append(str(takeaways))

    exercise = lesson.get("practicalExercise")
    if exercise:
        parts.append("## Practical Exercise")
        parts.append(_practical_exercise_to_markdown(exercise))

    resources = lesson.get("additionalResources")
    if resources:
        parts.append("## Additional Resources")
        parts.append(_resources_to_markdown(resources))

    return "\n\n".join(parts).strip()


def build_course_level_documents() -> List[Dict[str, Any]]:
    """
    Produces coarse documents describing each course (description, modules,
    lesson catalog) so queries like 'what courses are available' or
    'what is in the SIEM course' are answerable from the vector store.
    """
    catalog = load_course_catalog()
    documents: List[Dict[str, Any]] = []
    for slug, course in catalog.items():
        title = course.get("title", slug)
        description = course.get("description", "")

        course_doc = f"# {title}\n\n{description}\n\n"
        course_doc += (
            f"Difficulty: {course.get('difficulty', 'n/a')} | "
            f"Duration: {course.get('duration', 'n/a')}\n\n"
        )
        course_doc += "## Modules & Lessons\n"
        for module in course.get("modules", []):
            course_doc += (
                f"\n### Module {module.get('id')}: {module.get('title', '')}\n"
            )
            for lesson in module.get("lessons", []):
                course_doc += (
                    f"- Lesson {lesson.get('id')}: {lesson.get('title', '')} — "
                    f"{lesson.get('description', '')}\n"
                )
        documents.append({
            "text": course_doc.strip(),
            "doc_id": f"{slug}:course-overview",
            "metadata": {
                "kind": "course_overview",
                "course_slug": slug,
                "course_title": title,
                "lesson_id": "",
                "lesson_title": "",
                "source": _SOURCE_COURSE_META,
                "text": course_doc.strip(),
                "content_hash": content_hash(course_doc.strip()),
            },
        })
    return documents


def build_lesson_documents() -> List[Dict[str, Any]]:
    """
    Produces one raw document per lesson (full markdown body). Chunking happens
    later in the pipeline so the recursive markdown splitter can split on
    headings.
    """
    lessons_by_course = load_lesson_content()
    catalog = load_course_catalog()
    documents: List[Dict[str, Any]] = []
    for slug, lessons in lessons_by_course.items():
        course_meta = catalog.get(slug, {})
        course_title = course_meta.get("title", slug)
        display_id = _SLUG_DISPLAY_IDS.get(slug, slug)
        for lesson in lessons or []:
            lesson_id = lesson.get("id", "")
            lesson_title = lesson.get("title", "")
            body = lesson_to_markdown(lesson)
            if not body:
                continue
            documents.append({
                "text": body,
                "doc_id": f"{slug}:{lesson_id}:lesson",
                "metadata": {
                    "kind": "lesson",
                    "course_slug": slug,
                    "course_id": display_id,
                    "course_title": course_title,
                    "lesson_id": lesson_id,
                    "lesson_title": lesson_title,
                    "source": _SOURCE_LESSON_JSON,
                    "text": body,
                    "content_hash": content_hash(body),
                },
            })
    return documents


def build_all_static_documents() -> List[Dict[str, Any]]:
    """All static documents eligible for embedding (course overviews + lessons)."""
    docs = build_course_level_documents() + build_lesson_documents()
    logger.info(
        f"Static knowledge source produced {len(docs)} raw documents "
        f"({len(build_lesson_documents())} lessons, "
        f"{len(build_course_level_documents())} course overviews)."
    )
    return docs
