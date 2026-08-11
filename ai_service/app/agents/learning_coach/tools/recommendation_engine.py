from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.agents.learning_coach.models import LearningRecommendation, RecommendationPolicy, RecommendationExplanation
from app.platform.services.recommendation_service import RecommendationService
from app.platform.repositories.django_repository import DjangoPlatformRepository
from app.platform.services.platform_client import platform_client
from typing import Any

class RecommendationEngineTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="recommendation_engine",
            metadata=ToolMetadata(
                input_schema={"skill_profile": "SkillProfile", "policy": "RecommendationPolicy"},
                output_schema={"recommendations": "list"},
                tags=["learning_coach", "recommendation"]
            )
        )
        # Wire up the new Phase 8 services
        self.repo = DjangoPlatformRepository(platform_client)
        self.recommendation_service = RecommendationService(self.repo)

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        skill_profile = kwargs.get("skill_profile")
        
        # Use dummy token; in a real app, inject user's actual JWT
        token = "dummy_token"
        
        # Fetch real recommendations from Django platform
        platform_recs = await self.recommendation_service.generate_recommendations(token, "")
        
        recs = []
        for i, prec in enumerate(platform_recs):
            recs.append(
                LearningRecommendation(
                    id=prec.item_id,
                    title=prec.title,
                    type=prec.type.upper(),
                    priority=i+1,
                    rationale=prec.reason,
                    estimated_time_minutes=60,
                    difficulty=prec.difficulty,
                    prerequisites=[],
                    expected_impact="Skill improvement.",
                    explanation=RecommendationExplanation(
                        recommendation_id=prec.item_id,
                        recommendation_reason=prec.reason,
                        supporting_evidence="",
                        competency_gap_addressed="",
                        priority_reason="Platform Recommendation",
                        expected_outcome="Completion",
                        estimated_benefit="",
                        prerequisites=[],
                        confidence_score=0.9
                    )
                )
            )
            
        recs.sort(key=lambda x: (x.priority, x.title))
        return recs
