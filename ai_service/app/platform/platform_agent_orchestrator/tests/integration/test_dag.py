import pytest
import asyncio
from app.platform.platform_agent_orchestrator.agent import PlatformAgentOrchestrator

@pytest.mark.asyncio
async def test_integration_full_dag():
    orchestrator = PlatformAgentOrchestrator(orchestrator_service=None) # mock service
    response = await orchestrator.process_request("I need to investigate an IOC and trace network")
    
    assert response is not None
    assert response.summary == "Unified response generated successfully."
    # 2 capabilities returned from mocked intent tool
    assert len(response.detailed_sections) == 2 
