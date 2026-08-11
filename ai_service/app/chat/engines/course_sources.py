"""
Builds `course_sources` metadata for assistant responses.

When an answer is grounded in RAG chunks that belong to BlueTeamers lessons,
this module aggregates the retrieved chunks by COURSE — never one card per
chunk — so the frontend shows at most a few unique course cards, each listing
the referenced lessons grouped inside it.

Cards are emitted only for lesson-content chunks. Answers grounded in general
knowledge, external documentation, or small talk produce an empty list, so the
frontend renders nothing. Raw chunk metadata is never exposed.

This module never hardcodes course data (it reads the static course catalog)
and never generates HTML.
"""

import logging
from functools import lru_cache
from typing import Any, Dict, List, Optional

from app.knowledge.sources import load_course_catalog

logger = logging.getLogger("app.chat.engines.course_sources")

_SOURCE_LESSON_CONTENT = "lesson_content"
_MAX_COURSE_CARDS = 3

_LEVEL_LABELS = {
    "easy": "Beginner",
    "medium": "Intermediate",
    "intermediate": "Intermediate",
    "hard": "Advanced",
}


@lru_cache(maxsize=1)
def _get_catalog() -> Dict[str, Dict[str, Any]]:
    return load_course_catalog()


def _module_for_lesson(course_slug: str, lesson_id: str, catalog: Dict[str, Any]) -> str:
    course = catalog.get(course_slug)
    if not course:
        return ""
    for module in course.get("modules", []):
        for lesson in module.get("lessons", []):
            if str(lesson.get("id")) == str(lesson_id):
                return str(module.get("title", ""))
    return ""


def _document_metadata(doc: Any) -> Dict[str, Any]:
    if isinstance(doc, dict):
        return doc.get("metadata") or {}
    return getattr(doc, "metadata", None) or {}


def _document_score(doc: Any) -> float:
    try:
        if isinstance(doc, dict):
            return float(doc.get("score") or 0.0)
        return float(getattr(doc, "score", 0.0) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _course_label(index: int, level: str, progress: Optional[int], has_progress_data: bool) -> str:
    if index == 0:
        return "Best Match"
    if has_progress_data and progress is not None:
        return "Based on Your Progress"
    if has_progress_data and progress is None:
        return "Recommended Next"
    if level == "Advanced":
        return "Advanced Course"
    return "Covers this Topic"


def build_course_pointer(course_sources) -> str:
    """Short user-facing pointer to the module/lesson covering the answer.

    Returns an empty string when no lesson-content source was retrieved, so the
    prompt builder can simply skip the recommendation line.
    """
    if not course_sources:
        return ""
    top = course_sources[0]
    course_title = top.get("title")
    lessons = top.get("lessons") or []
    if not lessons:
        return course_title or ""
    first = lessons[0]
    module = first.get("module")
    lesson_title = first.get("title")
    parts = [p for p in (course_title, module, lesson_title) if p]
    if not parts:
        return ""
    if module:
        return f"Covered in Module '{module}' of {course_title} (Lesson: {lesson_title})"
    return f"Covered in {course_title} (Lesson: {lesson_title})"


def build_course_sources(
    documents: List[Any],
    progress_by_slug: Optional[Dict[str, int]] = None,
    max_courses: int = _MAX_COURSE_CARDS,
) -> List[Dict[str, Any]]:
    """
    Aggregates retrieved lesson chunks into one card per course.

    - Chunks are grouped by canonical course slug (deduplicated by lesson).
    - Courses are ranked by their best chunk similarity score (stable for
      dict-form documents where scores are unavailable).
    - The list is capped at `max_courses` (default 3) unique course cards.
    - Lessons inside a card are ordered by descending relevance.

    Each item in `documents` may be a Document-like object (`.metadata`/`.content`)
    or a raw dict (`{"content": ..., "metadata": {...}}`), so this works for every
    engine (RAG, Platform, AGENT).

    `progress_by_slug` optionally carries per-course completion percentages keyed
    by canonical course slug; when absent or unknown, `progress` stays null and the
    frontend simply hides the progress bar.
    """
    catalog = _get_catalog()
    progress_by_slug = progress_by_slug or {}

    # course_slug -> { score, lessons: {lesson_id: {title, module, score}}, order }
    courses: Dict[str, Dict[str, Any]] = {}

    for doc in documents:
        meta = _document_metadata(doc)
        if meta.get("source") != _SOURCE_LESSON_CONTENT:
            continue

        course_slug = meta.get("course_slug")
        lesson_id = meta.get("lesson_id")
        if not course_slug or not lesson_id:
            continue

        entry = courses.setdefault(course_slug, {
            "score": 0.0,
            "order": len(courses),
            "lessons": {},
            "display_id": "",
        })
        if not entry["display_id"]:
            entry["display_id"] = meta.get("course_id") or course_slug

        score = _document_score(doc)
        if score > entry["score"]:
            entry["score"] = score

        lesson_title = meta.get("lesson_title") or lesson_id
        lesson = entry["lessons"].get(lesson_id)
        if lesson is None:
            entry["lessons"][lesson_id] = {
                "id": lesson_id,
                "title": lesson_title,
                "module": _module_for_lesson(course_slug, lesson_id, catalog),
                "score": score,
            }
        else:
            lesson["score"] = max(lesson["score"], score)

    # Rank courses by best chunk score (stable sort preserves retrieval order for ties).
    ranked_slugs = sorted(
        courses,
        key=lambda slug: courses[slug]["score"],
        reverse=True,
    )[:_MAX_COURSE_CARDS]

    has_progress_data = bool(progress_by_slug)
    sources: List[Dict[str, Any]] = []

    for index, course_slug in enumerate(ranked_slugs):
        entry = courses[course_slug]
        course_meta = catalog.get(course_slug, {})

        level_raw = str(course_meta.get("difficulty", "") or "")
        level = _LEVEL_LABELS.get(level_raw.lower(), level_raw.title() if level_raw else "Beginner")
        duration = str(course_meta.get("duration", "") or "")

        progress = progress_by_slug.get(course_slug)
        if progress is None:
            progress = progress_by_slug.get(entry.get("display_id") or "")
        if progress is not None:
            progress = int(progress)

        # Lessons ordered by descending relevance; first is the "continue here" target.
        lessons = sorted(
            entry["lessons"].values(),
            key=lambda l: l["score"],
            reverse=True,
        )

        sources.append({
            "course_id": entry.get("display_id") or course_slug,
            "course_slug": course_slug,
            "title": course_meta.get("title")
            or next(iter(entry["lessons"].values()), {}).get("title")
            or course_slug,
            "label": _course_label(index, level, progress, has_progress_data),
            "rank": index + 1,
            "score": round(entry["score"], 4),
            "lessons": [
                {"id": l["id"], "title": l["title"], "module": l["module"]}
                for l in lessons
            ],
            "lessons_count": len(lessons),
            "progress": progress,
            "duration": duration,
            "level": level,
            "thumbnail": None,
            "rating": None,
            "action": {
                "label": "Continue Learning",
                "url": f"/courses/{course_slug}/lesson/{lessons[0]['id']}",
            },
            "course_action": {
                "label": "View Course",
                "url": f"/courses/{course_slug}",
            },
        })

    return sources
