import pytest
from app.agents.registry.agent_registry import AgentRegistry
from app.agents.models.agent_descriptor import AgentDescriptor, AgentStatus
from app.agents.models.capability import CapabilityModel
from app.agents.discovery.discovery_service import DiscoveryService

def test_discovery_ranking():
    registry = AgentRegistry()
    discovery = DiscoveryService(registry)
    
    # Agent 1: Available, priority 1, high cost
    agent1 = AgentDescriptor(
        name="Agent 1",
        status=AgentStatus.AVAILABLE,
        priority=1,
        cost_weight=10.0,
        capabilities=[CapabilityModel(capability_name="CODE")]
    )
    
    # Agent 2: Available, priority 2, low cost (Should win)
    agent2 = AgentDescriptor(
        name="Agent 2",
        status=AgentStatus.AVAILABLE,
        priority=2,
        cost_weight=1.0,
        capabilities=[CapabilityModel(capability_name="CODE")]
    )
    
    # Agent 3: Busy, priority 2
    agent3 = AgentDescriptor(
        name="Agent 3",
        status=AgentStatus.BUSY,
        priority=2,
        cost_weight=1.0,
        capabilities=[CapabilityModel(capability_name="CODE")]
    )
    
    # Agent 4: Offline
    agent4 = AgentDescriptor(
        name="Agent 4",
        status=AgentStatus.OFFLINE,
        priority=3,
        capabilities=[CapabilityModel(capability_name="CODE")]
    )
    
    registry.register(agent1)
    registry.register(agent2)
    registry.register(agent3)
    registry.register(agent4)
    
    ranked = discovery.discover_agents("CODE")
    
    assert len(ranked) == 3 # Offline is filtered out
    assert ranked[0].name == "Agent 2" # Highest priority, available, lowest cost
    assert ranked[1].name == "Agent 3" # Busy, but higher priority than Agent 1
    assert ranked[2].name == "Agent 1" # Available, but low priority and high cost
