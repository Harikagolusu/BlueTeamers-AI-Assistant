import pytest
import asyncio
from app.agents.orchestration.strategy_resolver import ExecutionStrategyResolver
from app.agents.coordinator.agent_coordinator import AgentCoordinator
from app.agents.planner.multi_agent_planner import MultiAgentPlanner
from app.agents.routing.agent_router import AgentRouter
from app.agents.registry.agent_registry import AgentRegistry
from app.agents.discovery.discovery_service import DiscoveryService
from app.agents.aggregation.aggregator import Aggregator
from app.planning.models.plan import ExecutionPlan, ExecutionStep, Capability
from app.planning.models.context import PlanningContext
from app.chat.context.execution_context import ExecutionContext
from app.models.chat.chat_models import ExecutionResult
from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.agents.interfaces.i_agent_executor_factory import IAgentExecutorFactory
from app.agents.models.agent_descriptor import AgentDescriptor, AgentStatus
from app.agents.models.capability import CapabilityModel

class MockSingleExecutor(IExecutionEngine):
    @property
    def name(self) -> str:
        return "MOCK_SINGLE"
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        return ExecutionResult.success("MOCK_SINGLE", "Single agent success")

class MockAgentExecutor(IExecutionEngine):
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
    @property
    def name(self) -> str:
        return f"MOCK_AGENT_{self.agent_id}"
    async def execute(self, context: ExecutionContext) -> ExecutionResult:
        return ExecutionResult.success("MOCK_AGENT", f"Delegated success from {self.agent_id}")

class MockExecutorFactory(IAgentExecutorFactory):
    def create_executor(self, agent: AgentDescriptor) -> IExecutionEngine:
        return MockAgentExecutor(agent.agent_id)

@pytest.mark.asyncio
async def test_strategy_resolver_and_coordinator():
    registry = AgentRegistry()
    discovery = DiscoveryService(registry)
    router = AgentRouter(discovery)
    factory = MockExecutorFactory()
    aggregator = Aggregator()
    coordinator = AgentCoordinator(router, factory, aggregator)
    planner = MultiAgentPlanner()
    
    resolver = ExecutionStrategyResolver(MockSingleExecutor(), coordinator, planner)
    
    # Register an agent for CODE capability
    agent = AgentDescriptor(
        name="Coder",
        capabilities=[CapabilityModel(capability_name="TOOL")] # Actually using TOOL capability from enum
    )
    registry.register(agent)
    
    # 1. Test Single Agent Route
    single_plan = ExecutionPlan(
        goal="Do one thing",
        steps=[ExecutionStep(name="Step 1", required_capability=Capability.TOOL)],
        capabilities_required=[Capability.TOOL]
    )
    context = ExecutionContext(metadata={"planning": PlanningContext(plan=single_plan)})
    
    result = await resolver.execute(context)
    assert result.message == "Single agent success"
    
    # 2. Test Multi Agent Route (forced)
    multi_plan = ExecutionPlan(
        goal="Do two things",
        steps=[
            ExecutionStep(name="Step 1", required_capability=Capability.TOOL),
            ExecutionStep(name="Step 2", required_capability=Capability.TOOL)
        ],
        capabilities_required=[Capability.TOOL],
        metadata={"force_multi_agent": True}
    )
    context.metadata["planning"] = PlanningContext(plan=multi_plan)
    
    result = await resolver.execute(context)
    assert result.success
    # Should contain messages from both delegates
    assert f"Delegated success from {agent.agent_id}" in result.message
