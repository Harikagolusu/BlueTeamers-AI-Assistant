from typing import Dict, Any, List
from app.platform.platform_agent_orchestrator.services.execution_state_machine import ExecutionStateMachine, ExecutionState
import time

class PlatformWorkflowBuilder:
    def __init__(self, tools_dict: Dict[str, Any]):
        self.tools = tools_dict
        
    async def run(self, context, request: str, orchestrator_service: Any, orch_context: Any):
        # 1. Analyze Intent
        intent_res = await self.tools["intent_analysis"].execute(context, request=request, orchestrator_context=orch_context)
        
        # 2. Resolve Capabilities & 3. Rank Candidate Agents (Wrapped in capability_resolution)
        cap_res = await self.tools["capability_resolution"].execute(context, capabilities=intent_res.requested_capabilities, orchestrator_context=orch_context)
        
        # 4. Generate Execution Plan
        plan_res = await self.tools["execution_planning"].execute(context, intent=intent_res, resolved_capabilities=cap_res, payload={"request": request})
        
        # 5. Validate Plan
        is_valid = await self.tools["plan_validation"].execute(context, execution_plan=plan_res)
        if not is_valid:
            raise Exception("Invalid execution plan")
            
        # 6. Optimize Plan
        plan_res = await self.tools["execution_optimization"].execute(context, execution_plan=plan_res)
        
        # 7. Generate Execution Schedule & 8. Generate Execution Queue (Wrapped in scheduling)
        queue_res = await self.tools["workflow_scheduling"].execute(context, execution_plan=plan_res)
        
        # 9. Execute Workflow (Invoke Agents) & 10. Monitor Execution State Machine & 11. Collect Results
        results = []
        for batch in queue_res.pending_batches:
            for inv in batch.invocations:
                # Mocking State Machine transitions
                step = next((s for s in plan_res.execution_steps if s.step_id == inv.invocation_id), None)
                if step:
                    ExecutionStateMachine.transition(step, ExecutionState.READY)
                    ExecutionStateMachine.transition(step, ExecutionState.RUNNING)
                    
                res = await self.tools["agent_invocation"].execute(context, invocation=inv, orchestrator_service=orchestrator_service)
                results.append(res)
                
                if step:
                    state = ExecutionState.COMPLETED if res.success else ExecutionState.FAILED
                    ExecutionStateMachine.transition(step, state)
                
        # 12. Aggregate Responses
        agg_res = await self.tools["response_aggregation"].execute(context, results=results)
        
        # 13. Store Metrics
        for res in results:
            await self.tools["metrics_collection"].execute(context, orchestrator_context=orch_context, latency=res.latency, step_name=res.step_id)
            
        # 14. Persist Execution History
        await self.tools["history_persistence"].execute(
            context, 
            workflow_id=orch_context.execution.workflow_id,
            request_id=orch_context.execution.request_id,
            status="COMPLETED",
            result=agg_res.model_dump()
        )
            
        # 15. Return Unified Response
        return agg_res
