import logging
import asyncio
import time
from typing import Optional, Dict, Any, List
from app.agents.base_interfaces import IAgentRegistry, IAgent
from app.agents.context import AgentContext
from app.shared.models.communication import AgentInvocation, AgentExecutionResult, AgentResponse, AgentExecutionMetrics, AgentRequest
from app.services.capabilities.capability_resolver import CapabilityResolver

logger = logging.getLogger(__name__)

class AgentOrchestrationService:
    """
    Reusable service for orchestrating execution of expert agents.
    Handles resolution, invocation, aggregation, failures, retries, and timeouts.
    """
    def __init__(self, agent_registry: IAgentRegistry, capability_resolver: Optional[CapabilityResolver] = None, default_timeout: int = 60, max_retries: int = 2):
        self.agent_registry = agent_registry
        self.capability_resolver = capability_resolver
        self.default_timeout = default_timeout
        self.max_retries = max_retries

    async def invoke_agent(self, invocation: AgentInvocation, base_context: AgentContext) -> AgentExecutionResult:
        """
        Resolves and invokes an expert agent using standardized communication models.
        Implements retries and timeouts.
        """
        agent_name = invocation.target_agent
        if not agent_name and invocation.target_capability and self.capability_resolver:
            agent_name = self.capability_resolver.resolve_name(invocation.target_capability)
            
        if not agent_name:
            logger.error("No target_agent or valid target_capability provided")
            return AgentExecutionResult(
                execution_id=invocation.context.execution_id,
                agent_name="unknown",
                success=False,
                response=AgentResponse(request_id=invocation.request.request_id, success=False, errors=["No agent target resolved."])
            )
            
        agent = self._resolve_agent(agent_name)
        if not agent:
            logger.error(f"Failed to resolve agent: {agent_name}")
            return AgentExecutionResult(
                execution_id=invocation.context.execution_id,
                agent_name=agent_name,
                success=False,
                response=AgentResponse(request_id=invocation.request.request_id, success=False, errors=[f"Agent {agent_name} not found in registry."])
            )

        eff_timeout = invocation.timeout_seconds or self.default_timeout
        session_id = invocation.context.session_id
        
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"[Session: {session_id}] Invoking {agent_name} (Attempt {attempt}/{self.max_retries})")
                
                start_time = time.time()
                # Execute agent with a timeout using handle_request if available, else fallback
                if hasattr(agent, "handle_request"):
                    response = await asyncio.wait_for(agent.handle_request(invocation.request, base_context), timeout=eff_timeout)
                else:
                    legacy_result = await asyncio.wait_for(agent.execute(base_context), timeout=eff_timeout)
                    response = AgentResponse(
                        request_id=invocation.request.request_id,
                        success=legacy_result.success,
                        data=legacy_result.response,
                        errors=legacy_result.errors,
                        warnings=legacy_result.warnings
                    )
                    
                duration = time.time() - start_time
                metrics = AgentExecutionMetrics(execution_time_ms=duration * 1000, retries=attempt - 1)
                
                if response.success:
                    logger.info(f"[Session: {session_id}] Agent {agent_name} executed successfully in {duration:.2f}s.")
                    return AgentExecutionResult(
                        execution_id=invocation.context.execution_id,
                        agent_name=agent_name,
                        success=True,
                        response=response,
                        metrics=metrics
                    )
                else:
                    logger.warning(f"[Session: {session_id}] Agent {agent_name} failed internally in {duration:.2f}s: {response.errors}")
                    
            except asyncio.TimeoutError:
                logger.warning(f"[Session: {session_id}] Timeout executing {agent_name} after {eff_timeout} seconds.")
            except Exception as e:
                logger.error(f"[Session: {session_id}] Unexpected error executing {agent_name}: {e}")

        logger.error(f"Agent {agent_name} failed after {self.max_retries} attempts.")
        return AgentExecutionResult(
            execution_id=invocation.context.execution_id,
            agent_name=agent_name,
            success=False,
            response=AgentResponse(request_id=invocation.request.request_id, success=False, errors=[f"Agent {agent_name} failed or timed out."])
        )

    async def invoke_agents_concurrently(self, invocations: List[AgentInvocation], base_context: AgentContext) -> Dict[str, AgentExecutionResult]:
        """
        Invokes multiple agents concurrently using invocations.
        """
        tasks = []
        for inv in invocations:
            tasks.append(self.invoke_agent(inv, base_context))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        aggregated = {}
        for inv, result in zip(invocations, results):
            name = inv.target_agent or (inv.target_capability.value if inv.target_capability else "unknown")
            if isinstance(result, Exception):
                logger.error(f"Concurrency error for {name}: {result}")
                aggregated[name] = AgentExecutionResult(
                    execution_id=inv.context.execution_id,
                    agent_name=name,
                    success=False,
                    response=AgentResponse(request_id=inv.request.request_id, success=False, errors=[str(result)])
                )
            else:
                aggregated[name] = result
                
        return aggregated

    def _resolve_agent(self, agent_name: str) -> Optional[IAgent]:
        return self.agent_registry.get(agent_name)
