from typing import Dict, Any
from app.platform.repositories.interfaces import IPlatformRepository
import logging

logger = logging.getLogger("app.platform.context.user_context")

class UserContextBuilder:
    def __init__(self, platform_repo: IPlatformRepository):
        self.platform_repo = platform_repo

    async def build(self, token: str) -> str:
        """
        Builds a compact user context string by querying the PlatformRepository
        for live data (profile, enrolled courses, progress, certificates).

        Kept intentionally sparse so the LLM spends tokens answering the user
        rather than re-reading a long platform block: only data that is actually
        present (and useful for personalizing answers) is included. Absent or
        unavailable values are skipped entirely instead of emitting filler lines.
        """
        profile_fields = []
        try:
            profile = await self.platform_repo.get_user_profile(token) if token else None
        except Exception as e:
            logger.error(f"Failed to fetch profile for user context: {e}")
            profile = None
        if profile:
            if profile.full_name:
                profile_fields.append(f"Name: {profile.full_name}")
            elif profile.email:
                profile_fields.append(f"Name: {profile.email}")

        try:
            enrolled = await self.platform_repo.get_enrolled_courses(token) if token else []
        except Exception as e:
            logger.error(f"Failed to fetch enrolled courses for user context: {e}")
            enrolled = []

        enrolled_lines = []
        progress_lines = []
        cert_lines = []
        if enrolled:
            for course in enrolled:
                enrolled_lines.append(course.title)
                try:
                    p = await self.platform_repo.get_progress(course.id, token)
                except Exception as e:
                    logger.error(f"Failed to fetch progress for {course.id}: {e}")
                    p = None
                if p and p.completed_lessons:
                    progress_lines.append(
                        f"{course.title}: {p.percent_complete}% ({len(p.completed_lessons)} lessons complete)"
                    )
        if enrolled_lines:
            profile_fields.append("Enrolled courses: " + ", ".join(enrolled_lines))
        if progress_lines:
            profile_fields.append("Course progress: " + "; ".join(progress_lines))

        if token:
            try:
                certificates = await self.platform_repo.get_certificates(token)
            except Exception as e:
                logger.error(f"Failed to fetch certificates for user context: {e}")
                certificates = []
            if certificates:
                cert_lines.append(", ".join([c.course_slug for c in certificates]))
                profile_fields.append("Certificates: " + "; ".join(cert_lines))

        if not profile_fields:
            return ""

        return "### User Platform Context ###\n" + "\n".join(profile_fields)