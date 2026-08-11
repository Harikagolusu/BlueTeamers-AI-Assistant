from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.chat.engines.suggested_courses import build_suggested_courses
from app.platform.repositories.interfaces import IPlatformRepository

import logging

logger = logging.getLogger("app.chat.pipeline.suggested_courses_stage")


class SuggestedCoursesStage(IExecutionStage):
    """Adds ``suggested_courses`` metadata to every AI response.

    Runs after the engine has produced its answer, so it is independent of the
    routed engine. It resolves the learner's enrollment (best-effort), builds
    top-N course recommendations for the query (only on strong topic match),
    and attaches them to the ExecutionResult metadata for the frontend's
    "Suggested BlueTeamers Courses" section.
    """

    def __init__(self, platform_repo: IPlatformRepository):
        self._platform_repo = platform_repo

    @property
    def name(self) -> str:
        return "SuggestedCourses"

    async def _resolve_enrolled(self, token) -> tuple:
        """Returns (enrolled_slugs, progress_by_slug). Never raises."""
        enrolled_slugs = set()
        progress_by_slug = {}
        if not token:
            return enrolled_slugs, progress_by_slug
        try:
            enrolled = await self._platform_repo.get_enrolled_courses(token)
            enrolled_slugs = {c.id for c in enrolled}
            for course in enrolled:
                try:
                    p = await self._platform_repo.get_progress(course.id, token)
                except Exception:
                    p = None
                if p and p.percent_complete is not None:
                    progress_by_slug[course.id] = p.percent_complete
        except Exception as e:
            logger.warning(f"Suggested-courses enrollment resolution failed: {e}")
        return enrolled_slugs, progress_by_slug

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        result = context.metadata.get("execution_result")
        if not result:
            return context

        query = context.metadata.get("query", "")
        token = context.metadata.get("token")

        enrolled_slugs, progress_by_slug = await self._resolve_enrolled(token)

        # Documents arrive as raw dicts on the ExecutionResult.
        documents = list(getattr(result, "documents", None) or [])
        try:
            suggested = build_suggested_courses(
                query,
                documents=documents,
                enrolled_slugs=enrolled_slugs,
                progress_by_slug=progress_by_slug,
            )
        except Exception as e:
            logger.warning(f"Suggested-courses build failed: {e}")
            suggested = []

        new_result = result.model_copy(update={
            "metadata": {**result.metadata, "suggested_courses": suggested},
        })
        new_metadata = {**context.metadata, "execution_result": new_result}
        return context.model_copy(update={"metadata": new_metadata})
