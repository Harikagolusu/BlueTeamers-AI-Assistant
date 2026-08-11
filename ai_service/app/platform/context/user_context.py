from typing import Dict, Any
from app.platform.repositories.interfaces import IPlatformRepository
import logging

logger = logging.getLogger("app.platform.context.user_context")

class UserContextBuilder:
    def __init__(self, platform_repo: IPlatformRepository):
        self.platform_repo = platform_repo

    async def build(self, token: str) -> str:
        """
        Builds a comprehensive user context string by querying the PlatformRepository
        for live data (profile, enrolled courses, progress, certificates).
        """
        context_parts = []
        context_parts.append("### User Platform Context ###")

        profile = enrolled = None
        try:
            profile = await self.platform_repo.get_user_profile(token) if token else None
        except Exception as e:
            logger.error(f"Failed to fetch profile for user context: {e}")
        try:
            enrolled = await self.platform_repo.get_enrolled_courses(token) if token else []
        except Exception as e:
            logger.error(f"Failed to fetch enrolled courses for user context: {e}")

        if profile and (profile.full_name or profile.email):
            context_parts.append(f"Name: {profile.full_name or profile.email}")
        else:
            context_parts.append("Name: Not available.")

        if enrolled:
            course_names = ", ".join([c.title for c in enrolled])
            context_parts.append(f"Active Enrollments: {course_names}")
        else:
            context_parts.append("Active Enrollments: None.")

        if enrolled and token:
            progress_strs = []
            for course in enrolled:
                try:
                    p = await self.platform_repo.get_progress(course.id, token)
                except Exception as e:
                    logger.error(f"Failed to fetch progress for {course.id}: {e}")
                    p = None
                if p and p.completed_lessons:
                    progress_strs.append(
                        f"{course.title} ({p.percent_complete}% - {len(p.completed_lessons)} lessons completed)"
                    )
            if progress_strs:
                context_parts.append("Recent Progress: " + "; ".join(progress_strs))
            else:
                context_parts.append("Recent Progress: No lessons completed yet.")
        else:
            context_parts.append("Recent Progress: Not available.")

        if token:
            try:
                certificates = await self.platform_repo.get_certificates(token)
            except Exception as e:
                logger.error(f"Failed to fetch certificates for user context: {e}")
                certificates = []
            if certificates:
                cert_strs = ", ".join([c.course_slug for c in certificates])
                context_parts.append(f"Certificates: {cert_strs}")
            else:
                context_parts.append("Certificates: None.")

        context_parts.append("Badges: This feature is not yet available on the platform.")
        context_parts.append("Learning Paths: This feature is not yet available on the platform.")

        return "\n".join(context_parts)
