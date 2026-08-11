"""Deterministic, engine-owned course recommendations.

Recommendations are owned by the engines (Platform Assistant / Learning Coach).
They deliberately do NOT rely on naive keyword matching against the query text or
RAG similarity for *relevance*. Instead relevance is derived from structured
signals:
  - the classified cyber domain (a router output, never raw query words),
  - static catalog metadata (level, domain tags),
  - the learner's actual platform state (enrollments, progress, certificates),
  - the learner's explicit request (e.g. "beginner" / "intermediate" level).

Each recommendation is enriched with a `course_sources`-shaped payload (course
slug + direct lesson deep-links from the static course catalog) so the frontend
can render a clickable lesson card, just like RAG-grounded answers.
"""
import logging
import re
from typing import Any, Dict, List, Optional, Tuple

from app.platform.repositories.interfaces import IPlatformRepository
from app.platform.models import Course, Recommendation
from app.chat.routing.domains import CyberDomain
from app.knowledge.sources import load_course_catalog

logger = logging.getLogger("app.platform.services.recommendation_service")

_LEVEL_RANK = {"beginner": 0, "intermediate": 1, "advanced": 2}

# Static catalog metadata used for deterministic scoring (independent of query text).
_COURSE_PROFILES = {
    "blue-team-soc-fundamentals": {"domains": ("soc", "monitoring", "foundation"), "level": "beginner"},
    "log-analysis-for-beginners": {"domains": ("log_analysis", "foundation"), "level": "beginner"},
    "siem-fundamentals": {"domains": ("siem", "monitoring", "foundation"), "level": "beginner"},
    "network-fundamentals": {"domains": ("network", "foundation"), "level": "beginner"},
    "network-security-monitoring": {"domains": ("network", "monitoring"), "level": "intermediate"},
    "incident-response-fundamentals": {"domains": ("incident_response",), "level": "intermediate"},
    "soc-analyst-path": {"domains": ("career", "soc"), "level": "intermediate"},
    "threat-hunting-fundamentals": {"domains": ("threat_hunting", "threat_intel"), "level": "advanced"},
    "detection-engineering-basics": {"domains": ("detection_engineering",), "level": "advanced"},
    "malware-analysis-fundamentals": {"domains": ("malware_analysis", "threat_intel"), "level": "advanced"},
}

# Which catalog domain tags matter for each cyber domain. PLATFORM and GENERAL map
# to an empty set -> progression ordering across the catalog (deterministic).
_DOMAIN_TAG_BY_CYBERDOMAIN = {
    CyberDomain.LEARNING: ("career", "soc", "foundation"),
    CyberDomain.KNOWLEDGE: ("foundation", "log_analysis", "siem", "network", "monitoring"),
    CyberDomain.THREAT_INTEL: ("threat_intel", "malware_analysis", "threat_hunting"),
    CyberDomain.INVESTIGATION: ("incident_response", "log_analysis", "threat_hunting"),
    CyberDomain.ASSESSMENT: ("detection_engineering", "incident_response", "siem"),
    CyberDomain.LAB: ("log_analysis", "siem", "threat_hunting"),
    CyberDomain.TOOLING: ("monitoring", "log_analysis"),
    CyberDomain.PLATFORM: (),
    CyberDomain.GENERAL: (),
}

_DEFAULT_TAGS = ("foundation", "log_analysis", "siem", "network", "soc", "monitoring")

# Query phrases that surface an explicit level preference. Mapped to normalized level.
_LEVEL_SIGNALS = {
    "beginner": ("beginner", "basic", "basics", "entry level", "start", "starting", "foundation",
                 "from scratch", "new to", "no experience", "first course", "level 1"),
    "intermediate": ("intermediate", "mid", "next level", "level 2", "continue"),
    "advanced": ("advanced", "expert", "senior", "level 3", "master"),
}

# Topic keywords (from query) -> catalog domain tags. Used to bias recommendations
# toward what the learner actually asked about.
_TOPIC_SIGNALS = {
    "network": ("network", "firewall", "tcp/ip", "networking", "subnet", "dns"),
    "siem": ("siem", "splunk", "elastic", "log ingestion", "alert"),
    "log_analysis": ("log", "log analysis", "logs", "event", "parse"),
    "soc": ("soc", "blue team", "security operations", "defensive"),
    "threat_intel": ("threat intel", "threat intelligence", "ioc", "cti", "tactics"),
    "incident_response": ("incident response", "ir", "response", "containment"),
    "malware_analysis": ("malware", "reverse engineering", "sandbox"),
    "threat_hunting": ("threat hunting", "hunting", "proactive"),
    "detection_engineering": ("detection", "sigma", "detection engineering"),
    "foundation": ("foundation", "basics", "fundamentals", "intro", "start"),
}


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def extract_requested_level(query: str) -> Optional[str]:
    """Return the explicit level preference in the query, if any.

    Returns one of "beginner" / "intermediate" / "advanced" or None when the user
    did not specify a level. This lets recommendations honour "for beginner".
    """
    norm = _norm(query)
    if not norm:
        return None
    for level, signals in _LEVEL_SIGNALS.items():
        for sig in signals:
            if f" {_norm(sig)} " in f" {norm} ":
                return level
    return None


def extract_topic_tags(query: str) -> Tuple[str, ...]:
    """Return catalog domain tags signalled by the query text (e.g. 'network')."""
    norm = _norm(query)
    if not norm:
        return ()
    matched = []
    for tag, signals in _TOPIC_SIGNALS.items():
        for sig in signals:
            if f" {_norm(sig)} " in f" {norm} ":
                matched.append(tag)
                break
    return tuple(matched)


def _catalog() -> Dict[str, Dict[str, Any]]:
    """Loaded (and cached) static course catalog."""
    return load_course_catalog()


def _lesson_links(course_slug: str, limit: int = 4) -> Tuple[List[Dict[str, Any]], str]:
    """Return (lessons, top_lesson_url) for a course from the static catalog.

    `lessons` items are `{id, title, module}` so they render inside a
    CourseSourceCard; the returned url deep-links to the first real lesson.
    """
    course = _catalog().get(course_slug)
    if not course:
        return [], ""
    lessons: List[Dict[str, Any]] = []
    for module in course.get("modules", []):
        module_title = module.get("title", "")
        for lesson in module.get("lessons", []):
            lid = str(lesson.get("id", ""))
            ltitle = lesson.get("title", "")
            if not lid or not ltitle:
                continue
            lessons.append({"id": lid, "title": ltitle, "module": module_title})
            if len(lessons) >= limit:
                break
        if len(lessons) >= limit:
            break
    top_url = f"/courses/{course_slug}/lesson/{lessons[0]['id']}" if lessons else ""
    return lessons, top_url


def _course_meta(slug: str) -> Dict[str, Any]:
    """Cached catalog metadata for a course slug (title, difficulty, duration)."""
    return _catalog().get(slug, {})


class RecommendationService:
    def __init__(self, platform_repo: IPlatformRepository):
        self.platform_repo = platform_repo

    async def generate_recommendations(
        self, token: str, context_query: str = ""
    ) -> List[Recommendation]:
        """Backward-compatible entry point; routes to the domain-aware path."""
        return await self.generate_for_domain(token, domain=None, query=context_query)

    async def generate_for_domain(
        self,
        token: str,
        domain: Optional[CyberDomain] = None,
        exclude_slugs: Optional[List[str]] = None,
        query: str = "",
    ) -> List[Recommendation]:
        try:
            all_courses = await self.platform_repo.get_courses(token)
        except Exception as e:
            logger.error(f"Failed to fetch courses for recommendations: {e}")
            all_courses = []

        if not all_courses:
            return []

        return await self._rank_courses(
            all_courses,
            token=token,
            domain=domain,
            exclude_slugs=exclude_slugs,
            query=query,
        )

    async def generate_from_catalog(
        self,
        query: str = "",
        domain: Optional[CyberDomain] = None,
    ) -> List[Recommendation]:
        """Recommend courses from the static BlueTeamers catalog (no user token).

        Used for logged-out / guest requests: recommendations come from the
        offline course catalog instead of the Django platform service, so the
        assistant can still suggest BlueTeamers courses and invite the user to
        enroll.
        """
        catalog = load_course_catalog()
        all_courses: List[Course] = []
        for slug, meta in catalog.items():
            profile = _COURSE_PROFILES.get(slug, {})
            all_courses.append(Course(
                slug=meta.get("slug") or slug,
                title=meta.get("title") or slug,
                description=meta.get("description") or "",
                level=(meta.get("difficulty") or profile.get("level") or "easy"),
                duration_hours=int(re.sub(r"[^0-9]", "", str(meta.get("duration") or "0")) or 0),
            ))

        if not all_courses:
            return []

        return await self._rank_courses(
            all_courses,
            token=None,
            domain=domain,
            exclude_slugs=None,
            query=query,
        )

    async def _rank_courses(
        self,
        all_courses: List[Course],
        token: Optional[str],
        domain: Optional[CyberDomain],
        exclude_slugs: Optional[List[str]],
        query: str,
    ) -> List[Recommendation]:
        target_tags = (
            _DOMAIN_TAG_BY_CYBERDOMAIN.get(domain, ()) if domain else ()
        ) or _DEFAULT_TAGS

        # Honour the learner's explicit request (e.g. "for beginner", "network").
        requested_level = extract_requested_level(query)
        query_tags = extract_topic_tags(query)
        if query_tags:
            # Combine domain tags with any topic tags the user actually asked about.
            target_tags = tuple(dict.fromkeys(target_tags + query_tags)) or target_tags

        exclude = set(exclude_slugs or [])
        learner_state = await self._learner_state(token, all_courses)
        exclude |= learner_state["enrolled"]

        scored: List[Tuple[float, Recommendation]] = []
        for course in all_courses:
            slug = (course.id or course.title or "").lower()
            if slug in exclude:
                continue
            profile = _COURSE_PROFILES.get(slug, {})
            course_tags = profile.get("domains", ())
            course_level = (profile.get("level") or (course.level or "beginner")).lower()

            score, reason = self._score_course(
                course_tags, course_level, target_tags, learner_state,
                requested_level=requested_level,
            )

            # Enrich with clickable lessons from the static course catalog.
            lessons, lesson_url = _lesson_links(slug)
            level_label = {
                "beginner": "Beginner", "intermediate": "Intermediate", "advanced": "Advanced",
            }.get(course_level, course_level.title() or "Beginner")
            scored.append((
                score,
                Recommendation(
                    type="course",
                    item_id=course.id,
                    course_slug=slug,
                    title=course.title,
                    reason=reason,
                    difficulty=course.level or course_level,
                    level=level_label,
                    score=float(score),
                    lessons=lessons,
                    lesson_url=lesson_url,
                    course_url=f"/courses/{slug}",
                ),
            ))

        scored.sort(key=lambda x: (x[0], x[1].title.lower()), reverse=True)
        return [r for _, r in scored[:3]]

    async def _learner_state(self, token: str, all_courses: List[Course]) -> dict:
        """Enrolled slugs + current level inferred from completed/enrolled courses."""
        enrolled_slugs: set = set()
        completed_levels: List[str] = []
        try:
            if token:
                enrolled = await self.platform_repo.get_enrolled_courses(token)
                enrolled_slugs = {c.id for c in enrolled}
                for course in enrolled:
                    p = None
                    try:
                        p = await self.platform_repo.get_progress(course.id, token)
                    except Exception:
                        pass
                    level = (_COURSE_PROFILES.get(course.id, {}).get("level")
                             or (course.level or "beginner").lower())
                    if p and p.percent_complete >= 90:
                        completed_levels.append(level)
        except Exception as e:
            logger.warning(f"Failed to build learner state for recommendations: {e}")

        completed_levels.sort(key=lambda l: _LEVEL_RANK.get(l, 0))
        current_level = completed_levels[-1] if completed_levels else "beginner"
        return {
            "enrolled": enrolled_slugs,
            "current_level": current_level,
            "has_enrollments": bool(enrolled_slugs),
        }

    @staticmethod
    def _score_course(
        course_tags,
        course_level,
        target_tags,
        learner_state,
        requested_level: Optional[str] = None,
    ) -> tuple:
        """Deterministic score: domain relevance + level fit + explicit request."""
        score = 0

        # 1. Domain relevance (structured catalog tags vs classified domain + query).
        tag_overlap = len(set(course_tags) & set(target_tags))
        score += tag_overlap * 3

        # 2. Level fit relative to the learner's inferred level.
        target_rank = _LEVEL_RANK.get(learner_state["current_level"], 0)
        course_rank = _LEVEL_RANK.get(course_level, 0)
        if course_rank == target_rank:
            score += 2
        elif course_rank == target_rank + 1:
            score += 1

        # 3. Honour an explicit level preference in the query (e.g. "for beginner").
        if requested_level:
            req_rank = _LEVEL_RANK.get(requested_level, 0)
            if course_rank == req_rank:
                score += 8
            elif course_rank < req_rank:
                score += 4
            elif course_rank == req_rank + 1:
                score += 1

        # 4. Progression: prefer unenrolled courses for learners with enrollments.
        if learner_state["has_enrollments"]:
            if course_level == "beginner" and not learner_state["enrolled"]:
                score += 1
        else:
            score += 1

        if requested_level and course_rank == _LEVEL_RANK.get(requested_level, 0):
            reason = f"A great {requested_level}-friendly course for you."
        elif tag_overlap >= 2:
            reason = "Directly matches your current focus area."
        elif tag_overlap == 1:
            reason = "Related to your current focus area."
        elif course_rank > target_rank:
            reason = "Natural next step in your learning progression."
        else:
            reason = "Solid foundation for your learning path."

        return score, reason
