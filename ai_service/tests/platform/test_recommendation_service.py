import pytest
from unittest.mock import AsyncMock

from app.chat.routing.domains import CyberDomain
from app.platform.models import Course, Recommendation
from app.platform.services.recommendation_service import RecommendationService


def _courses():
    return [
        Course(slug="blue-team-soc-fundamentals", title="Blue Team & SOC Fundamentals", description="d", level="easy", duration_hours=12),
        Course(slug="log-analysis-for-beginners", title="Log Analysis for Beginners", description="d", level="easy", duration_hours=8),
        Course(slug="siem-fundamentals", title="SIEM Fundamentals", description="d", level="easy", duration_hours=10),
        Course(slug="network-fundamentals", title="Network Fundamentals", description="d", level="easy", duration_hours=6),
        Course(slug="incident-response-fundamentals", title="Incident Response Fundamentals", description="d", level="medium", duration_hours=12),
        Course(slug="threat-hunting-fundamentals", title="Threat Hunting Fundamentals", description="d", level="hard", duration_hours=16),
        Course(slug="malware-analysis-fundamentals", title="Malware Analysis Fundamentals", description="d", level="hard", duration_hours=18),
    ]


def _service(repo=None):
    repo = repo or AsyncMock()
    return RecommendationService(repo)


@pytest.mark.asyncio
async def test_recommendations_do_not_depend_on_query_keyword_matching():
    repo = AsyncMock()
    repo.get_courses.return_value = _courses()
    repo.get_enrolled_courses.return_value = []
    service = _service(repo)

    # The query words are deliberately NOT present in any course title/description.
    recs = await service.generate_for_domain("some-token", domain=CyberDomain.THREAT_INTEL)

    assert len(recs) == 3
    assert isinstance(recs[0], Recommendation)
    # Threat-intel tagged courses (malware/threat-hunting) should lead.
    assert recs[0].item_id in ("malware-analysis-fundamentals", "threat-hunting-fundamentals")


@pytest.mark.asyncio
async def test_recommendations_exclude_enrolled_courses():
    repo = AsyncMock()
    repo.get_courses.return_value = _courses()
    repo.get_enrolled_courses.return_value = [
        Course(slug="siem-fundamentals", title="SIEM Fundamentals", description="d", level="easy", duration_hours=10)
    ]
    repo.get_progress.return_value = None
    service = _service(repo)

    recs = await service.generate_for_domain("some-token", domain=CyberDomain.PLATFORM)

    slugs = [r.item_id for r in recs]
    assert "siem-fundamentals" not in slugs
    assert len(recs) <= 3


@pytest.mark.asyncio
async def test_recommendations_deterministic_across_queries():
    repo = AsyncMock()
    repo.get_courses.return_value = _courses()
    repo.get_enrolled_courses.return_value = []
    service = _service(repo)

    recs_a = await service.generate_for_domain("t", domain=CyberDomain.LEARNING)
    recs_b = await service.generate_for_domain("t", domain=CyberDomain.LEARNING)

    assert [r.item_id for r in recs_a] == [r.item_id for r in recs_b]


@pytest.mark.asyncio
async def test_backward_compat_generate_recommendations_still_works():
    repo = AsyncMock()
    repo.get_courses.return_value = _courses()
    repo.get_enrolled_courses.return_value = []
    service = _service(repo)

    recs = await service.generate_recommendations("t", "anything at all")

    assert len(recs) == 3


@pytest.mark.asyncio
async def test_recommendations_honour_requested_beginner_level():
    repo = AsyncMock()
    repo.get_courses.return_value = _courses()
    repo.get_enrolled_courses.return_value = []
    service = _service(repo)

    recs = await service.generate_for_domain("t", query="suggest me some courses for beginner")

    assert len(recs) == 3
    # Every recommended course should be beginner-level when the user asked for beginner.
    beginner_slugs = {
        "blue-team-soc-fundamentals", "log-analysis-for-beginners",
        "siem-fundamentals", "network-fundamentals",
    }
    assert all(r.item_id in beginner_slugs for r in recs), [r.item_id for r in recs]


@pytest.mark.asyncio
async def test_recommendations_are_enriched_with_lesson_links():
    repo = AsyncMock()
    repo.get_courses.return_value = _courses()
    repo.get_enrolled_courses.return_value = []
    service = _service(repo)

    recs = await service.generate_for_domain("t", domain=CyberDomain.KNOWLEDGE)

    assert len(recs) >= 1
    top = recs[0]
    # Enrichment fields populate so the frontend can render clickable lesson cards.
    assert top.course_slug
    assert top.lesson_url.startswith("/courses/")
    assert top.course_url.startswith("/courses/")
    assert isinstance(top.lessons, list)
    assert len(top.lessons) > 0
    # Lessons carry id/title/module for the CourseSourceCard renderer.
    assert "id" in top.lessons[0]
    assert "title" in top.lessons[0]


@pytest.mark.asyncio
async def test_generate_from_catalog_works_without_token():
    service = _service(AsyncMock())

    recs = await service.generate_from_catalog(query="suggest me some courses for beginner")

    assert len(recs) == 3
    assert all(isinstance(r, Recommendation) for r in recs)
    # No repo call was made (catalog is offline).
    assert not service.platform_repo.get_courses.called
    # Beginner request -> only beginner-level catalog courses.
    beginner_slugs = {
        "blue-team-soc-fundamentals", "log-analysis-for-beginners",
        "siem-fundamentals", "network-fundamentals",
    }
    assert all(r.item_id in beginner_slugs for r in recs), [r.item_id for r in recs]
    assert recs[0].lesson_url.startswith("/courses/")
    assert len(recs[0].lessons) > 0

