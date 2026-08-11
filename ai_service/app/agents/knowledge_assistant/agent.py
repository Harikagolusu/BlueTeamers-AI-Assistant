from typing import Any, List, Dict
import time
import json
import uuid

from app.agents.base import BaseAgent
from app.agents.context import AgentContext
from app.agents.knowledge_assistant.models import (
    KnowledgeRequest, LearnerProfile, KnowledgeResponse, KnowledgeContext, 
    ExplanationLevel, LearningMetrics
)
from app.agents.knowledge_assistant.tools.concept_explanation import ConceptExplanationTool
from app.agents.knowledge_assistant.tools.concept_mapping import ConceptMappingTool
from app.agents.knowledge_assistant.tools.knowledge_retrieval import KnowledgeRetrievalTool
from app.agents.knowledge_assistant.tools.learning_path import LearningPathTool
from app.agents.knowledge_assistant.tools.knowledge_assessment import KnowledgeAssessmentTool
from app.agents.knowledge_assistant.tools.resource_recommendation import ResourceRecommendationTool
try:
    from app.services.workflow.workflow_builder import WorkflowBuilder
    from app.services.workflow.workflow_executor import WorkflowExecutor
    from app.services.workflow.workflow_context import WorkflowContext
except ImportError:
    # Fallback mock for testing
    WorkflowBuilder = None
    WorkflowExecutor = None
    WorkflowContext = None

class KnowledgeAssistantAgent(BaseAgent):
    """
    Educational agent focused on explaining cybersecurity concepts and guiding learners.
    """
    def __init__(self, manifest):
        super().__init__(manifest)
        self.ka_context = KnowledgeContext()
        self.tools_dict = {
            "concept_explanation": ConceptExplanationTool(),
            "concept_mapping": ConceptMappingTool(),
            "knowledge_retrieval": KnowledgeRetrievalTool(),
            "learning_path": LearningPathTool(),
            "knowledge_assessment": KnowledgeAssessmentTool(),
            "resource_recommendation": ResourceRecommendationTool()
        }

    async def initialize(self) -> None:
        self.ka_context = KnowledgeContext()
        if hasattr(self._context, "payload") and self._context.payload:
            payload = self._context.payload
            # Parse LearnerProfile if provided
            profile_data = payload.get("learner_profile", {})
            self.ka_context.profile = LearnerProfile(**profile_data) if profile_data else LearnerProfile()
            self.ka_context.raw_request = KnowledgeRequest(
                query=payload.get("query", ""),
                learner_profile=self.ka_context.profile
            )
        else:
            self.ka_context.profile = LearnerProfile()
            self.ka_context.raw_request = KnowledgeRequest(query="General concepts")

    async def retrieve(self) -> None:
        tool = self.tools_dict["knowledge_retrieval"]
        self.ka_context.retrieved_knowledge = await tool.execute(
            context=self._context, 
            query=self.ka_context.raw_request.query
        )

    async def select_tools(self) -> List[Any]:
        return list(self.tools_dict.values())

    async def execute_tools(self, tools: List[Any]) -> None:
        """
        Executes the educational workflow using the Workflow Engine.
        """
        async def explain_step(ctx: WorkflowContext):
            tool = self.tools_dict["concept_explanation"]
            res = await tool.execute(
                self._context, 
                concept=self.ka_context.raw_request.query,
                profile=self.ka_context.profile,
                retrieved_context=str(self.ka_context.retrieved_knowledge)
            )
            self.ka_context.explanation = res
            return res

        async def map_step(ctx: WorkflowContext):
            tool = self.tools_dict["concept_mapping"]
            res = await tool.execute(
                self._context,
                concept=self.ka_context.raw_request.query,
                known_concepts=self.ka_context.profile.known_concepts
            )
            self.ka_context.concept_map = res
            return res

        async def check_step(ctx: WorkflowContext):
            tool = self.tools_dict["knowledge_assessment"]
            res = await tool.execute(
                self._context,
                concept=self.ka_context.raw_request.query,
                level=self.ka_context.profile.experience_level.value
            )
            self.ka_context.knowledge_check = res
            return res
            
        async def recommend_step(ctx: WorkflowContext):
            tool = self.tools_dict["resource_recommendation"]
            res = await tool.execute(
                self._context,
                concept=self.ka_context.raw_request.query,
                level=self.ka_context.profile.experience_level.value
            )
            self.ka_context.recommendations = res
            return res

        async def path_step(ctx: WorkflowContext):
            tool = self.tools_dict["learning_path"]
            goals = ", ".join(self.ka_context.profile.learning_goals)
            res = await tool.execute(
                self._context,
                goal=goals,
                weak_topics=self.ka_context.profile.weak_topics,
                completed_topics=self.ka_context.profile.completed_topics
            )
            self.ka_context.learning_path = res
            return res

        if not WorkflowBuilder:
            # Fallback for playground/tests if executor isn't wired perfectly in this mocked codebase.
            wf_ctx = None
            await explain_step(wf_ctx)
            await map_step(wf_ctx)
            await check_step(wf_ctx)
            await recommend_step(wf_ctx)
            await path_step(wf_ctx)
            return

        builder = WorkflowBuilder(workflow_id=f"ka_flow_{uuid.uuid4()}")
        builder.add_function_step("explain", explain_step)
        builder.add_function_step("map", map_step, depends_on=["explain"])
        builder.add_function_step("check", check_step, depends_on=["explain"])
        builder.add_function_step("recommend", recommend_step, depends_on=["explain"])
        builder.add_function_step("path", path_step, depends_on=["map", "recommend"])

        executor = WorkflowExecutor(builder.build())
        wf_ctx = WorkflowContext(execution_id=self._context.execution_id)
        
        try:
            await executor.execute(wf_ctx)
        except Exception:
            await explain_step(wf_ctx)
            await map_step(wf_ctx)
            await check_step(wf_ctx)
            await recommend_step(wf_ctx)
            await path_step(wf_ctx)

    async def reason(self) -> Any:
        # LLM reasoning step aggregates the context into KnowledgeResponse
        exp = self.ka_context.explanation
        return KnowledgeResponse(
            summary=exp.summary if exp else "No summary available",
            detailed_explanation=exp.detailed_explanation if exp else "",
            real_world_example=exp.real_world_example if exp else "",
            visual_analogy=exp.visual_analogy if exp else "",
            common_mistakes=exp.common_mistakes if exp else [],
            detection_defense_notes=exp.detection_defense_notes,
            related_concepts=self.ka_context.concept_map.related_concepts if self.ka_context.concept_map else [],
            knowledge_check=self.ka_context.knowledge_check,
            recommended_resources=self.ka_context.recommendations,
            next_learning_topics=[step.topic for step in self.ka_context.learning_path.steps] if self.ka_context.learning_path else []
        )
        
    async def update_memory(self, final_response: str) -> None:
        self.ka_context.metrics.session_topics_covered.append(self.ka_context.raw_request.query)
        self.ka_context.metrics.questions_asked += 1
        
        # Convert response to string for base class if necessary
        return
        
    async def post_process(self, result: Any) -> str:
        # We just return the Pydantic model dumped to JSON
        if hasattr(result, "model_dump_json"):
            return result.model_dump_json()
        elif hasattr(result, "json"):
            return result.json()
        return json.dumps(result)
