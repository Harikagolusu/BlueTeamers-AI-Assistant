import pytest
from app.agents.registry.agent_registry import AgentRegistry
from app.agents.models.agent_descriptor import AgentDescriptor, AgentStatus
from app.agents.models.capability import CapabilityModel, ToolSupport

def test_agent_registry_crud():
    registry = AgentRegistry()
    
    agent = AgentDescriptor(
        name="Security Agent",
        capabilities=[CapabilityModel(capability_name="SECURITY_ANALYSIS")]
    )
    
    # Create
    registry.register(agent)
    assert len(registry.list_agents()) == 1
    
    # Read
    fetched = registry.get_agent(agent.agent_id)
    assert fetched.name == "Security Agent"
    
    # Capability lookup
    capable = registry.get_agents_by_capability("SECURITY_ANALYSIS")
    assert len(capable) == 1
    
    capable = registry.get_agents_by_capability("NOT_FOUND")
    assert len(capable) == 0
    
    # Delete
    registry.unregister(agent.agent_id)
    assert len(registry.list_agents()) == 0
