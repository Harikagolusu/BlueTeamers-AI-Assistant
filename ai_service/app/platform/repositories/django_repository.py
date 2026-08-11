import json
import logging
from functools import lru_cache
from typing import List, Optional
from app.platform.repositories.interfaces import IPlatformRepository
from app.platform.services.platform_client import PlatformApiClient
from app.platform.models import Course, Lab, LearningPath, Assessment, Certificate, Badge, Progress, Module, Lesson, UserProfile, Purchase
from app.core.exceptions import (
    DjangoUnavailableException,
    UnauthorizedException,
    NotFoundException,
    ValidationException,
    PlatformUnavailable,
    PlatformAuthenticationFailed,
    PlatformEndpointMissing
)

logger = logging.getLogger("app.platform.repositories.django_repository")

_PURCHASE_STATUS_PAID = "paid"


@lru_cache(maxsize=1)
def _static_lesson_counts() -> dict:
    """Map course slug -> total lesson count from the static course catalog."""
    try:
        with open("./app/knowledge/data/course_catalog.json") as f:
            catalog = json.load(f)
        counts = {}
        for entry in catalog.values():
            total = sum(len(m.get("lessons", [])) for m in entry.get("modules", []))
            for key in (entry.get("slug"), entry.get("id")):
                if key:
                    counts[key] = total
        return counts
    except Exception as e:
        logger.warning(f"Failed to load static lesson counts: {e}")
        return {}


class DjangoPlatformRepository(IPlatformRepository):
    def __init__(self, client: PlatformApiClient):
        self.client = client

    def _map_exception(self, e: Exception, resource: str):
        if isinstance(e, UnauthorizedException):
            raise PlatformAuthenticationFailed(f"Authentication failed for {resource}") from e
        elif isinstance(e, NotFoundException):
            raise PlatformEndpointMissing(f"Platform endpoint missing for {resource}") from e
        elif isinstance(e, DjangoUnavailableException):
            raise PlatformUnavailable(f"Platform unavailable when fetching {resource}") from e
        # Let other exceptions propagate natively (including ValidationException or unexpected errors)
        raise e

    async def get_user_profile(self, token: str) -> Optional[UserProfile]:
        # There is no GET /auth/profile/ endpoint (it is PATCH-only), so we derive the
        # profile from the validated access token via auth/verify/.
        try:
            data = await self.client.get("auth/verify/", token)
            return UserProfile(
                email=data.get("email"),
                full_name=data.get("full_name") or None,
                role=data.get("role") or None,
            )
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            self._map_exception(e, "profile")
            return None

    async def get_purchases(self, token: str) -> List[Purchase]:
        try:
            data = await self.client.get("payments/my-purchases/", token)
            purchases = []
            for p in data if isinstance(data, list) else []:
                purchases.append(Purchase(
                    course_slug=p.get("course_slug", ""),
                    status=p.get("status", ""),
                    amount=p.get("amount_inr"),
                    created_at=p.get("paid_at"),
                ))
            return purchases
        except Exception as e:
            logger.error(f"Error fetching purchases: {e}")
            self._map_exception(e, "purchases")
            return []

    async def get_courses(self, token: str) -> List[Course]:
        try:
            data = await self.client.get("courses/", token)
            return self._map_courses(data)
        except Exception as e:
            logger.error(f"Error fetching courses: {e}")
            self._map_exception(e, "courses")

    @staticmethod
    def _map_courses(data) -> List[Course]:
        courses = []
        for c in data if isinstance(data, list) else []:
            try:
                courses.append(Course(
                    slug=c.get("slug", ""),
                    title=c.get("title", ""),
                    description=c.get("description", ""),
                    level=c.get("level", ""),
                    duration_hours=int(c.get("duration_hours") or 0),
                ))
            except Exception as e:
                logger.warning(f"Skipping malformed course payload: {e}")
        return courses

    async def get_enrolled_courses(self, token: str) -> List[Course]:
        """Paid courses derived from purchases + the published catalog."""
        try:
            purchases = await self.get_purchases(token)
            catalog = await self.get_courses(token)
            paid_slugs = {p.course_slug for p in purchases if p.status == _PURCHASE_STATUS_PAID}
            # Bundle purchase grants access to the entire catalog.
            bundle_owned = any(
                p.course_slug == "all-courses-bundle" and p.status == _PURCHASE_STATUS_PAID
                for p in purchases
            )
            enrolled = []
            for course in catalog:
                if bundle_owned or course.id in paid_slugs:
                    enrolled.append(course)
            return enrolled
        except Exception as e:
            logger.error(f"Error fetching enrolled courses: {e}")
            return []

    async def get_course(self, slug: str, token: str) -> Optional[Course]:
        try:
            data = await self.client.get(f"courses/{slug}/", token)
            return self._map_courses([data])[0] if data else None
        except Exception as e:
            logger.error(f"Error fetching course {slug}: {e}")
            self._map_exception(e, f"course {slug}")

    async def get_labs(self, course_slug: str, token: str) -> List[Lab]:
        # The Django backend does not yet have a dedicated labs endpoint that returns Lab models.
        # It's mixed into lessons. We return an empty list for now until the backend supports it.
        return []

    async def get_learning_paths(self, token: str) -> List[LearningPath]:
        # This feature is not yet available on the platform (no DB model exists)
        return []

    async def get_assessments(self, course_slug: str, token: str) -> List[Assessment]:
        try:
            data = await self.client.get(f"courses/{course_slug}/quiz-scores/", token)
            # data is a list of quiz scores
            return [Assessment(id=str(q.get("quiz_id")), title=f"Quiz {q.get('quiz_id')}", course_slug=course_slug, passed=q.get("passed", False), score=q.get("score", 0)) for q in data] if isinstance(data, list) else []
        except Exception as e:
            logger.error(f"Error fetching assessments: {e}")
            self._map_exception(e, "assessments")

    async def get_certificates(self, token: str) -> List[Certificate]:
        """Certificates for each enrolled course, via certificates/my/<slug>/."""
        certificates = []
        try:
            enrolled = await self.get_enrolled_courses(token)
        except Exception as e:
            logger.error(f"Error fetching enrolled courses for certificates: {e}")
            enrolled = []
        for course in enrolled:
            try:
                data = await self.client.get(f"certificates/my/{course.id}/", token)
                if data and (data.get("exists") or data.get("certId")):
                    certificates.append(Certificate(
                        id=data.get("certId", course.id),
                        course_slug=course.id,
                        issued_at=data.get("issueDate", ""),
                        url=f"/verify/{data.get('certId', course.id)}",
                    ))
            except Exception as e:
                logger.debug(f"No certificate for {course.id}: {e}")
        return certificates

    async def get_badges(self, token: str) -> List[Badge]:
        # This feature is not yet available on the platform (no DB model exists)
        return []

    async def get_progress(self, course_slug: str, token: str) -> Optional[Progress]:
        try:
            data = await self.client.get(f"courses/{course_slug}/progress/", token)
            completed_ids = []
            if isinstance(data, list):
                completed_ids = [str(item.get("lesson_id")) for item in data if isinstance(item, dict) and item.get("lesson_id") is not None]
            elif isinstance(data, dict):
                completed_ids = data.get("completed_lessons", [])
            total = _static_lesson_counts().get(course_slug, 0)
            percent = int(round((len(completed_ids) / total) * 100)) if total else 0
            return Progress(course_slug=course_slug, percent_complete=percent, completed_lessons=completed_ids)
        except Exception as e:
            logger.error(f"Error fetching progress for {course_slug}: {e}")
            self._map_exception(e, "progress")

    async def search(self, query: str, token: str) -> List[Course]:
        try:
            data = await self.client.get(f"courses/?search={query}", token)
            return self._map_courses(data)
        except Exception as e:
            logger.error(f"Error searching courses: {e}")
            self._map_exception(e, "search")

