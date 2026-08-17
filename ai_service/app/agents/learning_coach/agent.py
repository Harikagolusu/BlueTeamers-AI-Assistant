from typing import Any, List
import uuid
import json

from app.agents.base import BaseAgent
from app.agents.learning_coach.models import (
    CoachingSession, LearnerProfile, LearningJourneyState, CoachingResponse, RecommendationPolicy
)
from app.agents.learning_coach.tools.learning_analytics import LearningAnalyticsTool
from app.agents.learning_coach.tools.skill_gap_analysis import SkillGapAnalysisTool
from app.agents.learning_coach.tools.roadmap_generation import RoadmapGenerationTool
from app.agents.learning_coach.tools.recommendation_engine import RecommendationEngineTool
from app.agents.learning_coach.tools.progress_forecast import ProgressForecastTool
from app.agents.learning_coach.tools.motivation_coaching import MotivationCoachingTool
from app.agents.learning_coach.tools.learning_pattern import LearningPatternTool
from app.agents.learning_coach.tools.goal_management import GoalManagementTool

try:
    from app.services.workflow.workflow_builder import WorkflowBuilder
    from app.services.workflow.workflow_executor import WorkflowExecutor
    from app.services.workflow.workflow_context import WorkflowContext
except ImportError:
    WorkflowBuilder = None
    WorkflowExecutor = None
    WorkflowContext = None

try:
    from app.observability.dependencies import get_observability_service
    obs = get_observability_service()
except ImportError:
    obs = None

class LearningCoachAgent(BaseAgent):
    """
    Personalized learning orchestrator for the entire educational platform.
    Coordinates other agents and builds long-term roadmaps.
    """
    def __init__(self, manifest, orchestration_service: Any = None):
        super().__init__(manifest)
        self.orchestration_service = orchestration_service
        self.session = CoachingSession(
            session_id=str(uuid.uuid4()),
            learner_profile=LearnerProfile(learner_id="default_learner")
        )
        self.tools_dict = {
            "analytics": LearningAnalyticsTool(),
            "skill_gaps": SkillGapAnalysisTool(),
            "roadmap": RoadmapGenerationTool(),
            "recommendations": RecommendationEngineTool(),
            "forecast": ProgressForecastTool(),
            "motivation": MotivationCoachingTool(),
            "patterns": LearningPatternTool(),
            "goals": GoalManagementTool()
        }

    async def initialize(self) -> None:
        if hasattr(self, "_context") and hasattr(self._context, "payload") and self._context.payload:
            self.user_query = self._context.payload.get("query", "")
        else:
            self.user_query = ""

    async def select_tools(self) -> List[Any]:
        return list(self.tools_dict.values())

    def _record_event(self, event_name: str, attributes: dict):
        if obs:
            obs.record_event(event_name, attributes)

    async def execute_tools(self, tools: List[Any]) -> None:
        import time
        from datetime import datetime, timezone
        from app.agents.learning_coach.models import JourneyTransition

        # Step 1: Understand Learner & Goals
        async def step_understand(ctx):
            start_time = time.time()
            self._record_event("goal_management", {"learner_id": self.session.learner_profile.learner_id})
            res = await self.tools_dict["goals"].execute(self._context, current_goals=self.session.learner_profile.goals, action="update", goal_details={})
            self.session.learner_profile.goals = res
            if obs:
                obs.record_metric("workflow_latency", time.time() - start_time, tags={"step": "understand"})
            return res

        # Step 2: Retrieve Learning History (Collaboration via Orchestrator)
        async def step_retrieve_history(ctx):
            start_time = time.time()
            self._record_event("collaboration_retrieval", {"target": "AssessmentCoach"})
            history = {}
            if self.orchestration_service:
                # STRICT BOUNDARY: Retrieve historical metrics ONLY. No active teaching/grading.
                history = await self.orchestration_service.get_historical_metrics("AssessmentCoach", self.session.learner_profile.learner_id)
                self.session.collaboration_history.append("AssessmentCoach_metadata")
            if obs:
                obs.record_metric("collaboration_latency", time.time() - start_time, tags={"step": "retrieve_history"})
            return history

        # Step 3: Analyze Learning Patterns
        async def step_patterns(ctx):
            start_time = time.time()
            self._record_event("pattern_analysis", {"learner_id": self.session.learner_profile.learner_id})
            res = await self.tools_dict["patterns"].execute(self._context, learner_id=self.session.learner_profile.learner_id, history={})
            self.session.patterns = res
            if obs:
                obs.record_metric("workflow_latency", time.time() - start_time, tags={"step": "patterns"})
            return res

        # Step 4: Analyze Skill Gaps
        async def step_skill_gaps(ctx):
            start_time = time.time()
            self._record_event("skill_gap_analysis", {"learner_id": self.session.learner_profile.learner_id})
            res = await self.tools_dict["skill_gaps"].execute(self._context, learner_id=self.session.learner_profile.learner_id, history={})
            self.session.learner_profile.skill_profile = res
            self.session.competency_summary = res
            if obs:
                obs.record_metric("workflow_latency", time.time() - start_time, tags={"step": "skill_gaps"})
            return res

        # Step 5: Generate Learning Analytics Snapshot
        async def step_analytics(ctx):
            start_time = time.time()
            self._record_event("analytics_generation", {"learner_id": self.session.learner_profile.learner_id})
            res = await self.tools_dict["analytics"].execute(self._context, learner_id=self.session.learner_profile.learner_id, history={})
            self.session.analytics_snapshot = res
            self.session.analytics = res.analytics
            if obs:
                obs.record_metric("analytics_latency", time.time() - start_time, tags={"step": "analytics"})
            return res

        # Step 6: Build Personalized Roadmap Version
        async def step_roadmap(ctx):
            start_time = time.time()
            self._record_event("roadmap_generation", {"learner_id": self.session.learner_profile.learner_id})
            res = await self.tools_dict["roadmap"].execute(self._context, goals=self.session.learner_profile.goals, skill_profile=self.session.learner_profile.skill_profile)
            self.session.roadmap_version = res
            self.session.roadmap = res
            if obs:
                obs.record_metric("roadmap_latency", time.time() - start_time, tags={"step": "roadmap"})
            return res

        # Step 7: Generate Recommendations
        async def step_recommendations(ctx):
            start_time = time.time()
            self._record_event("recommendation_generation", {"learner_id": self.session.learner_profile.learner_id})
            policy = RecommendationPolicy()
            res = await self.tools_dict["recommendations"].execute(self._context, skill_profile=self.session.learner_profile.skill_profile, policy=policy)
            self.session.recommendations = res
            if obs:
                obs.record_metric("recommendation_latency", time.time() - start_time, tags={"step": "recommendations"})
            return res

        # Step 8: Forecast Progress
        async def step_forecast(ctx):
            start_time = time.time()
            self._record_event("forecast_generation", {"learner_id": self.session.learner_profile.learner_id})
            res = await self.tools_dict["forecast"].execute(self._context, analytics=self.session.analytics, roadmap=self.session.roadmap)
            self.session.forecast = res
            if obs:
                obs.record_metric("forecast_latency", time.time() - start_time, tags={"step": "forecast"})
            return res

        # Step 9: Update Learning Journey & Step 10: Store Learning Metrics
        async def step_finalize(ctx):
            start_time = time.time()
            self._record_event("memory_update", {"session_id": self.session.session_id})
            
            # Transition Timeline Tracking
            previous = self.session.journey_state
            self.session.journey_state = LearningJourneyState.LEARNING
            if previous != self.session.journey_state:
                transition = JourneyTransition(
                    timestamp=datetime.now(timezone.utc),
                    previous_state=previous,
                    new_state=self.session.journey_state,
                    trigger="Roadmap execution active",
                    reason="Assigned tasks loaded for this session."
                )
                self.session.learner_profile.journey_timeline.append(transition)
            
            if obs:
                obs.record_metric("memory_update_latency", time.time() - start_time, tags={"step": "finalize"})
            return self.session.journey_state

        if not WorkflowBuilder:
            wf_ctx = None
            await step_understand(wf_ctx)
            await step_retrieve_history(wf_ctx)
            await step_patterns(wf_ctx)
            await step_skill_gaps(wf_ctx)
            await step_analytics(wf_ctx)
            await step_roadmap(wf_ctx)
            await step_recommendations(wf_ctx)
            await step_forecast(wf_ctx)
            await step_finalize(wf_ctx)
            return

        builder = WorkflowBuilder(workflow_id=f"lc_flow_{uuid.uuid4()}")
        builder.add_function_step("understand", step_understand)
        builder.add_function_step("retrieve_history", step_retrieve_history, depends_on=["understand"])
        builder.add_function_step("patterns", step_patterns, depends_on=["retrieve_history"])
        builder.add_function_step("skill_gaps", step_skill_gaps, depends_on=["patterns"])
        builder.add_function_step("analytics", step_analytics, depends_on=["skill_gaps"])
        builder.add_function_step("roadmap", step_roadmap, depends_on=["analytics"])
        builder.add_function_step("recommendations", step_recommendations, depends_on=["roadmap"])
        builder.add_function_step("forecast", step_forecast, depends_on=["recommendations"])
        builder.add_function_step("finalize", step_finalize, depends_on=["forecast"])

        executor = WorkflowExecutor(builder.build())
        wf_ctx = WorkflowContext(execution_id=self._context.execution_id if hasattr(self, "_context") and hasattr(self._context, "execution_id") else "default")
        
        try:
            await executor.execute(wf_ctx)
        except Exception:
            await step_understand(wf_ctx)
            await step_retrieve_history(wf_ctx)
            await step_patterns(wf_ctx)
            await step_skill_gaps(wf_ctx)
            await step_analytics(wf_ctx)
            await step_roadmap(wf_ctx)
            await step_recommendations(wf_ctx)
            await step_forecast(wf_ctx)
            await step_finalize(wf_ctx)

    async def reason(self) -> Any:
        message = await self.tools_dict["motivation"].execute(self._context, analytics=self.session.analytics, patterns=self.session.patterns)
        response = CoachingResponse(
            session_id=self.session.session_id,
            message=message,
            roadmap=self.session.roadmap,
            recommendations=self.session.recommendations,
            forecast=self.session.forecast
        )
        return response

    async def update_memory(self, final_response: str) -> None:
        self._record_event("longitudinal_memory_saved", {"session_id": self.session.session_id})
        return

    async def post_process(self, result: Any) -> str:
        if hasattr(result, "model_dump_json"):
            return result.model_dump_json()
        elif hasattr(result, "json"):
            return result.json()
        return json.dumps(result)
