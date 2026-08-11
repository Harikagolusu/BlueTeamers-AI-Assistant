"""
Data-driven cybersecurity relevance vocabulary derived from the course catalog.

The chat router uses this vocabulary as a *cybersecurity relevance gate*: a
query is treated as platform-relevant when it shares content-bearing terms with
course / module / lesson titles (and their descriptions) in the BlueTeamers
catalog. Building the gate from the catalog keeps it aligned with the actual
knowledge base instead of a hand-maintained keyword list.

This vocabulary only decides *whether* a query should run RAG retrieval. It
never decides *which* course to recommend — recommendations are always produced
by semantic retrieval over the knowledge base (see course_sources.py).
"""

import re
from functools import lru_cache
from typing import FrozenSet, List

from app.knowledge.sources import load_course_catalog

_WORD_RE = re.compile(r"[a-z0-9][a-z0-9+_/.-]*")

# Tokens that describe course structure or generic English rather than a
# cybersecurity topic. These would otherwise cause broad false positives
# (e.g. "financial analysis" matching "analysis").
_STOPWORDS = frozenset({
    "and", "for", "the", "with", "into", "from", "your", "you", "are", "this",
    "that", "what", "how", "why", "does", "can", "should", "will", "about",
    "their", "them", "they", "its", "not", "all", "any", "also",
    "introduction", "intro", "fundamentals", "basics", "essential", "essentials",
    "overview", "understanding", "understand", "learn", "learning", "module",
    "modules", "lesson", "lessons", "course", "courses", "full", "advanced",
    "beginner", "beginners", "part", "parts", "best", "practice", "practices",
    "practical", "hands", "deep", "dive", "analysis", "analyst", "analysts",
    "skills", "using", "use", "build", "building", "complete", "completion",
    "masterclass", "training", "series", "chapter", "chapters", "section",
    "sections", "final", "review", "mastery", "path", "paths", "level", "levels",
    "guide", "ultimate", "easy", "medium", "hard", "quiz", "quizzes", "exam",
    "tests", "workshop", "crash", "bootcamp", "category", "categories",
    "technology", "technologies", "general", "generic", "class", "classes",
    "foundation", "foundations", "step", "steps", "video", "videos", "readme",
    "day", "days", "week", "weeks", "hour", "hours", "minute", "minutes",
    # Generic programming / software vocabulary (not cybersecurity topics on
    # their own; the specific security terms remain covered by the domain
    # lexicon, e.g. "command and control", "injection", "shellcode").
    "write", "writing", "code", "python", "javascript", "java", "programming",
    "program", "script", "scripts", "scripting", "function", "functions",
    "variable", "variables", "string", "strings", "object", "objects",
    "array", "arrays", "syntax", "loop", "loops", "compiler", "library",
})


def _tokens(text: str) -> List[str]:
    return [t for t in _WORD_RE.findall(text.lower()) if len(t) >= 3 and t not in _STOPWORDS]


def _build_vocabulary(catalog) -> FrozenSet[str]:
    vocab = set()
    for course in catalog.values():
        if not isinstance(course, dict):
            continue
        for field in ("title", "shortTitle", "description"):
            vocab.update(_tokens(str(course.get(field) or "")))
        for module in course.get("modules", []):
            if isinstance(module, dict):
                vocab.update(_tokens(str(module.get("title") or "")))
                for lesson in module.get("lessons", []):
                    if isinstance(lesson, dict):
                        vocab.update(_tokens(str(lesson.get("title") or "")))
                        vocab.update(_tokens(str(lesson.get("description") or "")))
    return frozenset(vocab)


@lru_cache(maxsize=1)
def get_catalog_vocabulary() -> FrozenSet[str]:
    """Cached set of content-bearing tokens present in the course catalog."""
    return _build_vocabulary(load_course_catalog())


def _has_term(query_lower: str, term: str) -> bool:
    """Word-boundary aware presence check with simple plural handling."""
    if re.search(rf"\b{re.escape(term)}\b", query_lower):
        return True
    if not term.endswith(("s", "es", "ies")):
        if re.search(rf"\b{re.escape(term)}s\b", query_lower):
            return True
        if term.endswith("y") and len(term) > 1 and term[-2] not in "aeiou":
            if re.search(rf"\b{re.escape(term[:-1] + 'ies')}\b", query_lower):
                return True
    return False


def catalog_terms_in_query(query: str) -> List[str]:
    """Returns the catalog vocabulary terms present in `query` (whole words)."""
    query_lower = query.lower()
    return [t for t in get_catalog_vocabulary() if _has_term(query_lower, t)]
