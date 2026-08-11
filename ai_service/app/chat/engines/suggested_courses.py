"""Course recommendations for the "Suggested BlueTeamers Courses" section.

Instead of deep-linking into a lesson after every answer, this module
recommends the most relevant BlueTeamers COURSES for the learner's question
and returns clean course cards aware of the learner's enrollment status:

- Enrolled       -> "Continue Course" (resumes the course, or its first lesson
                    when progress exists)
- Not enrolled   -> "View Course" + "Enroll Course" (course detail / checkout)

Recommendations are only produced on a STRONG topic match:
  * a course whose lesson content was retrieved while answering, OR
  * a course whose catalog domains overlap the query's topic signals.
If neither applies, an empty list is returned so the frontend renders
nothing (we never recommend unrelated courses and never recommend after
every response).

Reuses the existing static course catalog and enrollment resolution. Raw
lesson bodies are never exposed for not-enrolled courses — cards carry only
public catalog metadata (title, description, difficulty, duration).
"""
import logging
import re
from typing import Any, Dict, List, Optional

from app.knowledge.sources import load_course_catalog
from app.chat.engines.course_sources import _LEVEL_LABELS, _document_metadata, _document_score

logger = logging.getLogger("app.chat.engines.suggested_courses")

_MAX_SUGGESTIONS = 3
# Only genuinely strong matches are recommended. Grounded (10+) and named
# (12+) courses always pass; catalog-tag-only courses need >= 2 overlapping
# domains (score >= 6) so we never pad a response to 3 unrelated cards.
_MIN_STRONG_SCORE = 6.0

# Imported lazily inside functions to avoid any import-cycle risk.
_profiles_cache = None


def _catalog() -> Dict[str, Dict[str, Any]]:
    return load_course_catalog()


def _profiles() -> Dict[str, Dict[str, Any]]:
    global _profiles_cache
    if _profiles_cache is None:
        try:
            from app.platform.services.recommendation_service import _COURSE_PROFILES
            _profiles_cache = dict(_COURSE_PROFILES)
        except Exception as e:  # pragma: no cover - defensive
            logger.warning(f"Course profiles unavailable: {e}")
            _profiles_cache = {}
    return _profiles_cache


def _extract_topic_tags(query: str):
    try:
        from app.platform.services.recommendation_service import extract_topic_tags
        return tuple(extract_topic_tags(query))
    except Exception as e:  # pragma: no cover - defensive
        logger.warning(f"Topic-tag extraction unavailable: {e}")
        return ()


def _resolve_named_course_slug(query: str) -> Optional[str]:
    """Best-effort: returns the catalog course a query explicitly names.

    Mirrors the learning-engines named-course resolution so a question like
    "notes on incident response fundamentals" is tied to that exact course.
    """
    from app.chat.intent.catalog_vocabulary import _tokens

    query_lower = query.lower()
    q_tokens = set(_tokens(query_lower))
    if not q_tokens:
        return None

    def _has(q_lower: str, token: str) -> bool:
        if re.search(rf"\b{re.escape(token)}\b", q_lower):
            return True
        if not token.endswith(("s", "es", "ies")):
            if re.search(rf"\b{re.escape(token)}s\b", q_lower):
                return True
        return False

    best_slug, best_score, second_score = None, 0, 0
    for slug, meta in _catalog().items():
        if not isinstance(meta, dict):
            continue
        from app.chat.intent.catalog_vocabulary import _tokens as _tok
        title_tokens = set(_tok(str(meta.get("title") or "")))
        slug_tokens = {t for t in _tok(slug.replace("-", " "))}
        signature = title_tokens | slug_tokens
        if not signature:
            continue
        score = sum(1 for t in signature if _has(query_lower, t))
        if score > best_score:
            second_score = best_score
            best_slug, best_score = slug, score
        elif score == best_score and score > 0:
            second_score = score
    if best_score >= 2 or (best_score == 1 and second_score == 0):
        return best_slug
    return None


def _first_lesson_id(slug: str) -> Optional[str]:
    """First lesson id of a course (used as the "continue here" deep link)."""
    for module in _catalog().get(slug, {}).get("modules", []):
        for lesson in module.get("lessons", []):
            lid = str(lesson.get("id", "") or "")
            if lid:
                return lid
    return None


def _build_card(
    course_slug: str,
    enrolled: bool,
    progress: Optional[int],
    score: float,
    rank: int,
) -> Dict[str, Any]:
    meta = _catalog().get(course_slug, {})
    level_raw = str(meta.get("difficulty", "") or "")
    level = _LEVEL_LABELS.get(level_raw.lower(), level_raw.title() if level_raw else "Beginner")
    duration = str(meta.get("duration") or "N/A")

    course_url = f"/courses/{course_slug}"
    first_lesson = _first_lesson_id(course_slug)
    # Enrolled learners resume from the course (or first lesson when progress
    # exists); not-enrolled learners get separate View / Enroll actions.
    if enrolled:
        lesson_url = f"{course_url}/lesson/{first_lesson}" if progress and first_lesson else course_url
    else:
        lesson_url = None

    return {
        "course_id": meta.get("id") or course_slug,
        "course_slug": course_slug,
        "title": meta.get("title") or course_slug,
        "description": meta.get("description") or "",
        "level": level,
        "duration": duration,
        "enrolled": bool(enrolled),
        "progress": progress,
        "rank": rank,
        "score": round(float(score), 4),
        "course_url": course_url,
        "lesson_url": lesson_url,
        "enroll_url": f"{course_url}/checkout",
        "action": {
            "label": "Continue Course" if enrolled else "Enroll Course",
            "url": lesson_url if enrolled else f"{course_url}/checkout",
        },
        "course_action": {"label": "View Course", "url": course_url},
    }


def build_suggested_courses(
    query: str,
    documents: Optional[List[Any]] = None,
    enrolled_slugs=None,
    progress_by_slug=None,
    max_courses: int = _MAX_SUGGESTIONS,
) -> List[Dict[str, Any]]:
    """Build top-N course suggestions for a query.

    ``documents`` are the raw retrieved documents (dicts or Document-like
    objects); ``enrolled_slugs`` is the set of canonical course slugs the
    learner is enrolled in; ``progress_by_slug`` optionally carries per-course
    completion percentages. Returns an empty list when there is no strong
    topic match.
    """
    documents = list(documents or [])
    enrolled_slugs = set(enrolled_slugs or [])
    progress_by_slug = progress_by_slug or {}
    catalog = _catalog()
    profiles = _profiles()

    query_tags = set(_extract_topic_tags(query))
    named_course = _resolve_named_course_slug(query)

    # Grounded courses: lesson content that was actually retrieved to answer.
    grounded: Dict[str, float] = {}
    for doc in documents:
        meta = _document_metadata(doc)
        if meta.get("source") != "lesson_content":
            continue
        slug = meta.get("course_slug")
        if not slug:
            continue
        grounded[slug] = max(grounded.get(slug, 0.0), _document_score(doc))

    # Score candidate courses.
    scored: List[tuple] = []
    seen = set()

    def _register(slug: str, score: float, overlap: set, grounded_score: float):
        if slug not in catalog:
            return
        if slug in seen:
            return
        seen.add(slug)
        scored.append((score, slug, overlap, grounded_score))

    for slug, doc_score in grounded.items():
        overlap = set(profiles.get(slug, {}).get("domains", ())) & query_tags
        # Grounded is a strong signal; topic overlap adds relevance.
        score = 10.0 + min(doc_score, 1.0) * 5.0 + len(overlap) * 3.0
        _register(slug, score, overlap, doc_score)

    if named_course and named_course not in seen:
        overlap = set(profiles.get(named_course, {}).get("domains", ())) & query_tags
        score = 12.0 + len(overlap) * 3.0
        _register(named_course, score, overlap, 0.0)

    for slug, profile in profiles.items():
        if slug in seen or slug not in catalog:
            continue
        overlap = set(profile.get("domains", ())) & query_tags
        if not overlap:
            continue
        score = len(overlap) * 3.0
        _register(slug, score, overlap, 0.0)

    # Only strong matches are recommended; never recommend unrelated courses.
    strong = [s for s in scored if s[0] >= _MIN_STRONG_SCORE]
    if not strong:
        return []

    strong.sort(key=lambda s: (s[0], s[2]), reverse=True)
    strong = strong[:max_courses]

    cards = []
    for rank, (score, slug, overlap, grounded_score) in enumerate(strong, start=1):
        enrolled = slug in enrolled_slugs
        progress = progress_by_slug.get(slug)
        if progress is not None:
            try:
                progress = int(progress)
            except (TypeError, ValueError):
                progress = None
        cards.append(_build_card(
            slug,
            enrolled=enrolled,
            progress=progress,
            score=score,
            rank=rank,
        ))
    return cards
