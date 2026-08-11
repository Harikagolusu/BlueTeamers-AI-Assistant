import asyncio
import logging
from typing import Optional
from app.platform.repositories.interfaces import IPlatformRepository
from app.platform.services.recommendation_service import RecommendationService
from app.llm.interfaces import ILLMService
from app.prompt_builder.simple_prompt_builder import SimplePromptBuilder
from app.models.chat.chat_models import SessionInitializationResponse, PlatformContextPayload
from app.platform.models import UserProfile, Course, Progress, Purchase, Recommendation

logger = logging.getLogger("app.chat.services.session_initializer")

class SessionInitializer:
    def __init__(self, platform_repo: IPlatformRepository, recommendation_service: RecommendationService, llm: ILLMService, prompt_builder: SimplePromptBuilder):
        self.platform_repo = platform_repo
        self.recommendation_service = recommendation_service
        self.llm = llm
        self.prompt_builder = prompt_builder
        # Simple local dictionary cache: token -> SessionInitializationResponse
        self._session_cache = {}

    async def initialize_session(self, token: str) -> SessionInitializationResponse:
        if not token:
            raise ValueError("Token is required for session initialization")
            
        # Temporary bypass cache to ensure fresh data
        # if token in self._session_cache:
        #     logger.info("Session cache hit. Returning cached session initialization.")
        #     return self._session_cache[token]
            
        logger.info("Fetching platform context concurrently...")
        # Execute concurrent Django API calls
        profile_task = asyncio.create_task(self.platform_repo.get_user_profile(token))
        purchases_task = asyncio.create_task(self.platform_repo.get_purchases(token))
        all_courses_task = asyncio.create_task(self.platform_repo.get_courses(token))
        
        results = await asyncio.gather(profile_task, purchases_task, all_courses_task, return_exceptions=True)
        
        if isinstance(results[0], Exception):
            logger.error(f"Failed to fetch profile: {results[0]}")
            profile = None
        else:
            profile = results[0]
            
        if isinstance(results[1], Exception):
            logger.error(f"Failed to fetch purchases: {results[1]}")
            purchases = []
        else:
            purchases = results[1]
            
        if isinstance(results[2], Exception):
            logger.error(f"Failed to fetch courses: {results[2]}")
            all_courses = []
        else:
            all_courses = results[2]
        
        # Build courses and fetch progress concurrently
        active_courses = []
        progress_tasks = []
        for p in purchases:
            course = next((c for c in all_courses if c.id == p.course_slug), None)
            if course:
                active_courses.append(course)
                progress_tasks.append(asyncio.create_task(self.platform_repo.get_progress(course.id, token)))
                
        progress_list = []
        if progress_tasks:
            progress_results = await asyncio.gather(*progress_tasks, return_exceptions=True)
            for pr in progress_results:
                if isinstance(pr, Exception):
                    logger.error(f"Failed to fetch progress: {pr}")
                elif pr is not None:
                    progress_list.append(pr)
                
        # Generate recommendations
        recommendations = await self.recommendation_service.generate_recommendations(token, "next activity")
        
        # Build prompt
        name = profile.full_name if profile and profile.full_name else "User"
        course_names = ", ".join([c.title for c in active_courses])
        progress_hint = ""
        if progress_list:
            pct = int(sum(p.percent_complete for p in progress_list) / len(progress_list))
            progress_hint = f"They have on average {pct}% progress across their courses."
        prompt = (
            "You are BlueTeamers, the AI Workspace of the BlueTeamers enterprise cybersecurity "
            "learning platform — an experienced SOC mentor, not a generic chatbot.\n"
            f"The user's name is {name}.\n"
            f"They are enrolled in the following courses: {course_names}.\n"
            f"{progress_hint}\n"
            "Write a short, engaging welcome message that greets them as a cybersecurity "
            "mentor would open a session. Mention their name and, if available, their "
            "enrolled courses or progress briefly. Offer a concrete starting point "
            "(e.g. reviewing course material, practicing a concept, or diving into a "
            "security topic like MITRE ATT&CK or log analysis). Keep it to 2-4 sentences, "
            "no markdown, professional and encouraging."
        )
        
        welcome_message = await self.llm.generate(prompt)
        
        payload = PlatformContextPayload(
            profile=profile,
            courses=active_courses,
            progress=progress_list,
            recommendations=recommendations,
            certificates=[]
        )
        
        response = SessionInitializationResponse(
            welcome_message=welcome_message,
            platform_context=payload
        )
        
        self._session_cache[token] = response
        return response
