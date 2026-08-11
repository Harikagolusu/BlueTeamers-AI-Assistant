import asyncio
from typing import List
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.planning.models.plan import ExecutionPlan, ExecutionStep
from app.planning.models.context import PlanningContext
from app.agents.interfaces.i_agent_coordinator import IAgentCoordinator
from app.agents.interfaces.i_agent_router import IAgentRouter
from app.agents.interfaces.i_agent_executor_factory import IAgentExecutorFactory
from app.agents.interfaces.i_aggregator import IAggregator
from app.agents.models.orchestration_models import MultiAgentExecutionPlan, AgentTask, CoordinationState

class AgentCoordinator(IAgentCoordinator):
    """
    Coordinates multi-agent execution. Does not execute logic directly; delegates to AgentExecutors.
    """
    def __init__(
        self,
        router: IAgentRouter,
        executor_factory: IAgentExecutorFactory,
        aggregator: IAggregator
    ):
        self._router = router
        self._executor_factory = executor_factory
        self._aggregator = aggregator

    async def coordinate(self, multi_plan: MultiAgentExecutionPlan, context: ExecutionContext) -> ExecutionResult:
        multi_plan.state = CoordinationState.ROUTING
        
        # 1. Routing Phase
        tasks: List[AgentTask] = []
        for step in multi_plan.original_execution_plan.steps:
            agent = self._router.route_step(step)
            if not agent:
                return ExecutionResult.failed("COORDINATOR", [{"error": f"No agent found for capability {step.required_capability.value}"}])
                
            task = AgentTask(
                step_id=step.step_id,
                assigned_agent_id=agent.agent_id
            )
            tasks.append(task)
            
        multi_plan.delegated_tasks = tasks
        multi_plan.state = CoordinationState.EXECUTING
        
        # 2. Execution Phase (For simplicity, executing sequentially in this prototype, 
        # but could easily use asyncio.gather for independent steps in DAG)
        results: List[ExecutionResult] = []
        
        for task in tasks:
            task.status = CoordinationState.EXECUTING
            
            # Find the original step
            step = next(s for s in multi_plan.original_execution_plan.steps if s.step_id == task.step_id)
            
            # Create a single-step ExecutionPlan for the delegated agent
            sub_plan = ExecutionPlan(
                goal=step.name,
                steps=[step],
                capabilities_required=[step.required_capability]
            )
            
            # Inject it into a new PlanningContext
            sub_metadata = context.metadata.copy()
            sub_metadata["planning"] = PlanningContext(plan=sub_plan)
            
            # Also inform the executor which agent it represents
            sub_metadata["agent_id"] = task.assigned_agent_id
            
            sub_context = ExecutionContext(
                correlation_id=context.correlation_id,
                trace_id=context.trace_id,
                metadata=sub_metadata,
                permissions=context.permissions
            )
            
            # Create an executor configured for this specific agent via factory
            # Need a dummy AgentDescriptor based on assigned_agent_id
            from app.agents.models.agent_descriptor import AgentDescriptor
            agent_desc = AgentDescriptor(agent_id=task.assigned_agent_id, name="Delegated Agent")
            
            executor = self._executor_factory.create_executor(agent_desc)
            
            try:
                # Execute the sub-plan
                result = await executor.execute(sub_context)
                task.result = result
                task.status = CoordinationState.COMPLETED if result.success else CoordinationState.FAILED
                
                # Tag metadata
                if result.metadata is None:
                    result.metadata = {}
                result.metadata["agent_id"] = task.assigned_agent_id
                
                results.append(result)
                
                if not result.success:
                    # Break on failure in sequential execution
                    multi_plan.state = CoordinationState.FAILED
                    return self._aggregator.aggregate(results)
            except Exception as e:
                task.status = CoordinationState.FAILED
                multi_plan.state = CoordinationState.FAILED
                results.append(ExecutionResult.failed("COORDINATOR", [{"error": str(e)}]))
                return self._aggregator.aggregate(results)
                
        # 3. Aggregation Phase
        multi_plan.state = CoordinationState.AGGREGATING
        final_result = self._aggregator.aggregate(results)
        
        multi_plan.state = CoordinationState.COMPLETED
        return final_result
