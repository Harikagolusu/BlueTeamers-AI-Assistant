from typing import Any
import uuid
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.models import OrchestratorContext, ExecutionContext, ExecutionMetadata
from app.platform.platform_agent_orchestrator.workflow import PlatformWorkflowBuilder
from app.platform.platform_agent_orchestrator.repositories.execution_history import InMemoryExecutionHistoryRepository
from app.platform.platform_agent_orchestrator.tools import *

class PlatformAgentOrchestrator:
    def __init__(self, orchestrator_service: Any = None):
        self.orchestrator_service = orchestrator_service
        self.history_repo = InMemoryExecutionHistoryRepository()
        self.tools = {
            "intent_analysis": IntentAnalysisTool(),
            "capability_resolution": CapabilityResolutionTool(),
            "execution_planning": ExecutionPlanningTool(),
            "plan_validation": PlanValidationTool(),
            "execution_optimization": ExecutionOptimizationTool(),
            "workflow_scheduling": WorkflowSchedulingTool(),
            "agent_invocation": AgentInvocationTool(),
            "response_aggregation": ResponseAggregationTool(),
            "failure_recovery": FailureRecoveryTool(),
            "context_management": ContextManagementTool(),
            "metrics_collection": MetricsCollectionTool(),
            "history_persistence": HistoryPersistenceTool(self.history_repo)
        }
        self.workflow = PlatformWorkflowBuilder(self.tools)
        
    async def process_request(self, request: str) -> Any:
        req_id = f"req-{uuid.uuid4().hex[:8]}"
        wf_id = f"wf-{uuid.uuid4().hex[:8]}"
        
        context = ToolContext(execution_id=req_id)
        orch_context = OrchestratorContext(
            execution=ExecutionContext(request_id=req_id, workflow_id=wf_id),
            metadata=ExecutionMetadata(request_id=req_id, workflow_id=wf_id)
        )
        
        return await self.workflow.run(context, request, self.orchestrator_service, orch_context)
