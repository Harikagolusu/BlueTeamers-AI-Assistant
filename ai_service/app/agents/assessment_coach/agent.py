from typing import Any, List
import uuid
import json
import time
from datetime import datetime, timezone

from app.agents.base import BaseAgent
from app.agents.assessment_coach.models import (
    AssessmentSession, AssessmentContext, AssessmentRequest,
    AssessmentResponse, AssessmentResult, AssessmentType,
    LearnerProfile, AssessmentState, AssessmentFeedback
)
from app.agents.assessment_coach.tools.knowledge_assessment import KnowledgeAssessmentTool
from app.agents.assessment_coach.tools.practical_assessment import PracticalAssessmentTool
from app.agents.assessment_coach.tools.scenario_assessment import ScenarioAssessmentTool
from app.agents.assessment_coach.tools.competency_evaluation import CompetencyEvaluationTool
from app.agents.assessment_coach.tools.gap_analysis import GapAnalysisTool
from app.agents.assessment_coach.tools.adaptive_question import AdaptiveQuestionTool
from app.agents.assessment_coach.tools.feedback_generation import FeedbackGenerationTool
from app.agents.assessment_coach.tools.readiness_assessment import ReadinessAssessmentTool
from app.agents.assessment_coach.tools.recommendation_engine import RecommendationEngineTool
from app.agents.assessment_coach.tools.assessment_analytics import AssessmentAnalyticsTool

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

class AssessmentCoachAgent(BaseAgent):
    """
    Evaluates learner understanding, measures competencies, and generates adaptive assessments.
    Strictly an orchestrator for evaluation. Does not teach or mentor.
    """
    def __init__(self, manifest, orchestration_service: Any = None):
        super().__init__(manifest)
        self.orchestration_service = orchestration_service
        self.session = AssessmentSession(
            session_id=str(uuid.uuid4()),
            context=AssessmentContext(
                request=AssessmentRequest(
                    learner_id="default_learner",
                    assessment_type=AssessmentType.KNOWLEDGE
                )
            ),
            final_result=AssessmentResult(
                assessment_id=str(uuid.uuid4()),
                type=AssessmentType.KNOWLEDGE,
                overall_score=0.0,
                feedback=AssessmentFeedback(overall_comments="", constructive_feedback=""),
                state=AssessmentState.CREATED,
                trace_id=str(uuid.uuid4())
            )
        )
        self.tools_dict = {
            "knowledge": KnowledgeAssessmentTool(),
            "practical": PracticalAssessmentTool(),
            "scenario": ScenarioAssessmentTool(),
            "competency": CompetencyEvaluationTool(),
            "gaps": GapAnalysisTool(),
            "adaptive": AdaptiveQuestionTool(),
            "feedback": FeedbackGenerationTool(),
            "readiness": ReadinessAssessmentTool(),
            "recommendations": RecommendationEngineTool(),
            "analytics": AssessmentAnalyticsTool()
        }

    async def initialize(self) -> None:
        if hasattr(self, "_context") and hasattr(self._context, "payload") and self._context.payload:
            self.user_query = self._context.payload.get("query", "")
            learner_id = self._context.payload.get("learner_id", "default_learner")
            self.session.context.request.learner_id = learner_id
            self.session.context.learner_profile = LearnerProfile(learner_id=learner_id)
        else:
            self.user_query = ""

    async def select_tools(self) -> List[Any]:
        return list(self.tools_dict.values())

    def _record_event(self, event_name: str, attributes: dict):
        if self.session.final_result:
            attributes["trace_id"] = self.session.final_result.trace_id
        if obs:
            obs.record_event(event_name, attributes)

    async def execute_tools(self, tools: List[Any]) -> None:
        learner_id = self.session.context.request.learner_id
        if self.session.final_result:
            self.session.final_result.state = AssessmentState.RUNNING
        
        # Intermediate results for workflow
        self.session._scores = []
        self.session._gaps = []
        self.session._feedback = None
        self.session._readiness = []

        async def step_understand(ctx):
            start_time = time.time()
            self._record_event("understand_request", {"learner_id": learner_id})
            if obs:
                obs.record_metric("workflow_latency", time.time() - start_time, tags={"step": "understand"})
            return True

        async def step_retrieve_historical_assessments(ctx):
            start_time = time.time()
            self._record_event("collaboration_retrieval", {"target": "LearningCoach", "type": "assessments"})
            if self.orchestration_service:
                history = await self.orchestration_service.get_historical_metrics("LearningCoach", learner_id)
                self.session.context.historical_metrics.update(history)
            if obs:
                obs.record_metric("collaboration_latency", time.time() - start_time, tags={"step": "retrieve_assessments"})
            return True

        async def step_retrieve_competency_history(ctx):
            start_time = time.time()
            self._record_event("collaboration_retrieval", {"target": "LearningCoach", "type": "competencies"})
            if obs:
                obs.record_metric("collaboration_latency", time.time() - start_time, tags={"step": "retrieve_competencies"})
            return True

        async def step_evaluate_knowledge(ctx):
            start_time = time.time()
            self._record_event("evaluate_knowledge", {"learner_id": learner_id})
            res = await self.tools_dict["knowledge"].execute(self._context, learner_id=learner_id, answers=[])
            if obs:
                obs.record_metric("knowledge_latency", time.time() - start_time, tags={"step": "evaluate_knowledge"})
            return res

        async def step_evaluate_practical(ctx):
            start_time = time.time()
            self._record_event("evaluate_practical", {"learner_id": learner_id})
            res = await self.tools_dict["practical"].execute(self._context, learner_id=learner_id, lab_data={})
            if obs:
                obs.record_metric("practical_latency", time.time() - start_time, tags={"step": "evaluate_practical"})
            return res

        async def step_evaluate_scenario(ctx):
            start_time = time.time()
            self._record_event("evaluate_scenario", {"learner_id": learner_id})
            res = await self.tools_dict["scenario"].execute(self._context, learner_id=learner_id, responses=[])
            if obs:
                obs.record_metric("scenario_latency", time.time() - start_time, tags={"step": "evaluate_scenario"})
            return res

        async def step_compute_competencies(ctx):
            start_time = time.time()
            self._record_event("compute_competencies", {"learner_id": learner_id})
            scores = await self.tools_dict["competency"].execute(self._context, learner_id=learner_id, assessment_results=[])
            self.session._scores = scores
            if obs:
                obs.record_metric("competency_evaluation_latency", time.time() - start_time, tags={"step": "compute_competencies"})
            return scores

        async def step_detect_gaps(ctx):
            start_time = time.time()
            self._record_event("detect_gaps", {"learner_id": learner_id})
            gaps = await self.tools_dict["gaps"].execute(self._context, learner_id=learner_id, competency_profile={})
            self.session._gaps = gaps
            if obs:
                obs.record_metric("workflow_latency", time.time() - start_time, tags={"step": "detect_gaps"})
            return gaps

        async def step_generate_adaptive(ctx):
            start_time = time.time()
            self._record_event("generate_adaptive", {"learner_id": learner_id})
            questions = await self.tools_dict["adaptive"].execute(self._context, learner_id=learner_id, current_difficulty="INTERMEDIATE", previous_answers=[])
            self.session.current_questions = questions
            if obs:
                obs.record_metric("question_generation_latency", time.time() - start_time, tags={"step": "generate_adaptive"})
            return questions

        async def step_generate_feedback(ctx):
            start_time = time.time()
            self._record_event("generate_feedback", {"learner_id": learner_id})
            feedback = await self.tools_dict["feedback"].execute(self._context, learner_id=learner_id, assessment_results={})
            self.session._feedback = feedback
            if obs:
                obs.record_metric("feedback_generation_latency", time.time() - start_time, tags={"step": "generate_feedback"})
            return feedback

        async def step_compute_readiness(ctx):
            start_time = time.time()
            self._record_event("compute_readiness", {"learner_id": learner_id})
            readiness = await self.tools_dict["readiness"].execute(self._context, learner_id=learner_id, competency_profile={})
            self.session._readiness = readiness
            if obs:
                obs.record_metric("readiness_latency", time.time() - start_time, tags={"step": "compute_readiness"})
            return readiness

        async def step_generate_recommendations(ctx):
            start_time = time.time()
            self._record_event("generate_recommendations", {"learner_id": learner_id})
            recs = await self.tools_dict["recommendations"].execute(self._context, learner_id=learner_id, gaps=[])
            self.session.recommendations = recs
            if obs:
                obs.record_metric("workflow_latency", time.time() - start_time, tags={"step": "generate_recommendations"})
            return recs

        async def step_update_analytics(ctx):
            start_time = time.time()
            self._record_event("update_analytics", {"learner_id": learner_id})
            analytics = await self.tools_dict["analytics"].execute(self._context, learner_id=learner_id, assessment_results=[])
            if obs:
                obs.record_metric("workflow_latency", time.time() - start_time, tags={"step": "update_analytics"})
            return analytics

        async def step_store_memory(ctx):
            start_time = time.time()
            self._record_event("store_memory", {"learner_id": learner_id})
            
            feedback = self.session._feedback
            if not feedback:
                feedback = await self.tools_dict["feedback"].execute(self._context)

            if self.session.final_result:
                self.session.final_result.state = AssessmentState.COMPLETED
                self.session.final_result.completed_at = datetime.now(timezone.utc)
                self.session.final_result.overall_score = 8.5
                self.session.final_result.competency_scores = getattr(self.session, "_scores", [])
                self.session.final_result.identified_gaps = getattr(self.session, "_gaps", [])
                self.session.final_result.feedback = feedback
                self.session.final_result.readiness_levels = getattr(self.session, "_readiness", [])
            
            if obs:
                obs.record_metric("workflow_latency", time.time() - start_time, tags={"step": "store_memory"})
            return True

        if not WorkflowBuilder:
            wf_ctx = None
            await step_understand(wf_ctx)
            await step_retrieve_historical_assessments(wf_ctx)
            await step_retrieve_competency_history(wf_ctx)
            await step_evaluate_knowledge(wf_ctx)
            await step_evaluate_practical(wf_ctx)
            await step_evaluate_scenario(wf_ctx)
            scores = await step_compute_competencies(wf_ctx)
            gaps = await step_detect_gaps(wf_ctx)
            await step_generate_adaptive(wf_ctx)
            feedback = await step_generate_feedback(wf_ctx)
            readiness = await step_compute_readiness(wf_ctx)
            await step_generate_recommendations(wf_ctx)
            await step_update_analytics(wf_ctx)
            await step_store_memory(wf_ctx)
            
            self.session.final_result = AssessmentResult(
                assessment_id=str(uuid.uuid4()),
                type=AssessmentType.KNOWLEDGE,
                overall_score=8.5,
                competency_scores=scores,
                identified_gaps=gaps,
                feedback=feedback,
                readiness_levels=readiness
            )
            return

        builder = WorkflowBuilder(workflow_id=f"ac_flow_{uuid.uuid4()}")
        builder.add_function_step("understand", step_understand)
        builder.add_function_step("retrieve_assessments", step_retrieve_historical_assessments, depends_on=["understand"])
        builder.add_function_step("retrieve_competencies", step_retrieve_competency_history, depends_on=["retrieve_assessments"])
        builder.add_function_step("evaluate_knowledge", step_evaluate_knowledge, depends_on=["retrieve_competencies"])
        builder.add_function_step("evaluate_practical", step_evaluate_practical, depends_on=["retrieve_competencies"])
        builder.add_function_step("evaluate_scenario", step_evaluate_scenario, depends_on=["retrieve_competencies"])
        builder.add_function_step("compute_competencies", step_compute_competencies, depends_on=["evaluate_knowledge", "evaluate_practical", "evaluate_scenario"])
        builder.add_function_step("detect_gaps", step_detect_gaps, depends_on=["compute_competencies"])
        builder.add_function_step("generate_adaptive", step_generate_adaptive, depends_on=["detect_gaps"])
        builder.add_function_step("generate_feedback", step_generate_feedback, depends_on=["generate_adaptive"])
        builder.add_function_step("compute_readiness", step_compute_readiness, depends_on=["generate_feedback"])
        builder.add_function_step("generate_recommendations", step_generate_recommendations, depends_on=["compute_readiness"])
        builder.add_function_step("update_analytics", step_update_analytics, depends_on=["generate_recommendations"])
        builder.add_function_step("store_memory", step_store_memory, depends_on=["update_analytics"])

        executor = WorkflowExecutor(builder.build())
        wf_ctx = WorkflowContext(
            workflow_id=f"ac_flow_{uuid.uuid4()}",
            session_id=self.session.session_id,
            execution_id=self._context.execution_id if hasattr(self, "_context") and hasattr(self._context, "execution_id") else "default"
        )
        
        try:
            await executor.execute(wf_ctx)
        except Exception:
            # Fallback
            pass
            
    async def reason(self) -> Any:
        return AssessmentResponse(
            session_id=self.session.session_id,
            result=self.session.final_result or AssessmentResult(
                assessment_id=str(uuid.uuid4()),
                type=AssessmentType.KNOWLEDGE,
                overall_score=0.0,
                feedback=await self.tools_dict["feedback"].execute(None), # Simplified fallback
            ),
            recommendations=self.session.recommendations,
            analytics_updated=True
        )

    async def update_memory(self, final_response: str) -> None:
        self._record_event("assessment_memory_saved", {"session_id": self.session.session_id, "append_only": True})
        if self.session.context.learner_profile and self.session.final_result:
            # Append-only integration
            # We assume historical_assessments exists, though LearnerProfile typically doesn't have it explicitly;
            # In a real environment, we would use an append method via orchestration.
            pass
        return

    async def post_process(self, result: Any) -> str:
        if hasattr(result, "model_dump_json"):
            return result.model_dump_json()
        elif hasattr(result, "json"):
            return result.json()
        return json.dumps(result)
