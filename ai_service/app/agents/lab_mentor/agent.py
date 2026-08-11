from typing import Any, List
import uuid
import json

from app.agents.base import BaseAgent
from app.services.lab.models import (
    LabSession, LabState, HintLevel
)
from app.agents.lab_mentor.tools.lab_analysis import LabAnalysisTool
from app.agents.lab_mentor.tools.progress_tracking import ProgressTrackingTool
from app.agents.lab_mentor.tools.mistake_detection import MistakeDetectionTool
from app.agents.lab_mentor.tools.hint_generation import HintGenerationTool
from app.agents.lab_mentor.tools.hint_validation import HintValidationTool
from app.agents.lab_mentor.tools.lab_planning import LabPlanningTool
from app.agents.lab_mentor.tools.reflection import ReflectionTool

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

class LabMentorAgent(BaseAgent):
    """
    Flagship educational agent that adaptively guides learners through labs without revealing answers.
    """
    def __init__(self, manifest):
        super().__init__(manifest)
        self.session = LabSession(
            session_id=str(uuid.uuid4()),
            learner_id="default_learner",
            lab_id="unknown"
        )
        self.tools_dict = {
            "analysis": LabAnalysisTool(),
            "tracking": ProgressTrackingTool(),
            "mistakes": MistakeDetectionTool(),
            "hinting": HintGenerationTool(),
            "validation": HintValidationTool(),
            "planning": LabPlanningTool(),
            "reflection": ReflectionTool()
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
        async def step_analysis(ctx):
            old_state = self.session.current_state
            res = await self.tools_dict["analysis"].execute(
                self._context, 
                user_query=self.user_query,
                current_state=self.session.current_state
            )
            self.session.current_state = res
            if old_state != res:
                self._record_event("state_transition", {"old": old_state.value, "new": res.value})
                if res == LabState.COMPLETED:
                    self._record_event("completion_event", {"lab_id": self.session.lab_id})
            return res

        async def step_tracking(ctx):
            res = await self.tools_dict["tracking"].execute(
                self._context, 
                history=self.session.attempt_history,
                metrics=self.session.learning_metrics,
                action=self.user_query
            )
            self.session.attempt_history = res["history"]
            self.session.learning_metrics = res["metrics"]
            return res

        async def step_mistakes(ctx):
            res = await self.tools_dict["mistakes"].execute(self._context, action=self.user_query)
            self.blocker = res.get("blocker", "")
            category = res.get("category")
            if category and category.value != "UNKNOWN":
                self.session.attempt_history.mistake_category = category
                self._record_event("mistake_classification", {"category": category.value})
            if self.blocker and self.blocker != "No obvious blocker detected.":
                self._record_event("blocker_detection", {"blocker": self.blocker})
            return res

        async def step_hinting(ctx):
            # Adaptive Hint level
            level = HintLevel.LEVEL_1
            if self.session.attempt_history.hint_requests > 2:
                level = HintLevel.LEVEL_3
            elif self.session.attempt_history.hint_requests > 1:
                level = HintLevel.LEVEL_2
                
            res = await self.tools_dict["hinting"].execute(self._context, blocker=getattr(self, "blocker", ""), level=level)
            self.session.current_hint = res
            self._record_event("hint_request", {"level": level.value})
            return res

        async def step_validation(ctx):
            if not self.session.current_hint:
                return
            res = await self.tools_dict["validation"].execute(self._context, hint_content=self.session.current_hint.content)
            if not res["is_safe"]:
                self.session.is_leakage_detected = True
                self.session.current_hint.content = "Generic conceptual hint. (Original hint suppressed due to leakage)"
                self.session.learning_metrics.hints_rewritten += 1
                self._record_event("hint_rewrite", {"reason": res["feedback"]})
            return res

        async def step_planning(ctx):
            res = await self.tools_dict["planning"].execute(
                self._context, 
                history=self.session.attempt_history, 
                state=self.session.current_state
            )
            self.session.feedback = res
            return res

        async def step_reflection(ctx):
            res = await self.tools_dict["reflection"].execute(self._context, action=self.user_query)
            self.session.reflection = res
            self._record_event("reflection_generation", {"concept": res.expected_concept})
            return res

        if not WorkflowBuilder:
            wf_ctx = None
            await step_analysis(wf_ctx)
            await step_tracking(wf_ctx)
            await step_mistakes(wf_ctx)
            await step_hinting(wf_ctx)
            await step_validation(wf_ctx)
            await step_planning(wf_ctx)
            await step_reflection(wf_ctx)
            return

        builder = WorkflowBuilder(workflow_id=f"lm_flow_{uuid.uuid4()}")
        builder.add_function_step("analysis", step_analysis)
        builder.add_function_step("tracking", step_tracking, depends_on=["analysis"])
        builder.add_function_step("mistakes", step_mistakes, depends_on=["tracking"])
        builder.add_function_step("hinting", step_hinting, depends_on=["mistakes"])
        builder.add_function_step("validation", step_validation, depends_on=["hinting"])
        builder.add_function_step("planning", step_planning, depends_on=["validation"])
        builder.add_function_step("reflection", step_reflection, depends_on=["planning"])

        executor = WorkflowExecutor(builder.build())
        wf_ctx = WorkflowContext(execution_id=self._context.execution_id if hasattr(self, "_context") and hasattr(self._context, "execution_id") else "default")
        try:
            await executor.execute(wf_ctx)
        except Exception:
            await step_analysis(wf_ctx)
            await step_tracking(wf_ctx)
            await step_mistakes(wf_ctx)
            await step_hinting(wf_ctx)
            await step_validation(wf_ctx)
            await step_planning(wf_ctx)
            await step_reflection(wf_ctx)

    async def reason(self) -> Any:
        return {
            "session_id": self.session.session_id,
            "state": self.session.current_state.value,
            "hint": self.session.current_hint.model_dump() if self.session.current_hint else None,
            "feedback": self.session.feedback.model_dump() if self.session.feedback else None,
            "reflection": self.session.reflection.model_dump() if self.session.reflection else None,
            "metrics": self.session.learning_metrics.model_dump(),
            "history": self.session.attempt_history.model_dump()
        }

    async def update_memory(self, final_response: str) -> None:
        if self.session.reflection:
            self.session.attempt_history.reflections_completed += 1
        return

    async def post_process(self, result: Any) -> str:
        if hasattr(result, "model_dump_json"):
            return result.model_dump_json()
        elif hasattr(result, "json"):
            return result.json()
        return json.dumps(result)
