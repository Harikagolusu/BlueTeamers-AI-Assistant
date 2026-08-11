import pytest
import asyncio
from app.platform.platform_agent_orchestrator.agent import PlatformAgentOrchestrator

@pytest.mark.asyncio
async def test_platform_agent_orchestrator_investigation():
    orchestrator = PlatformAgentOrchestrator(orchestrator_service=None)
    response = await orchestrator.process_request("I need to investigate an IOC")
    
    assert response is not None
    assert response.summary == "Unified response generated successfully."
    assert len(response.detailed_sections) > 0
    
@pytest.mark.asyncio
async def test_platform_agent_orchestrator_general_chat():
    orchestrator = PlatformAgentOrchestrator(orchestrator_service=None)
    response = await orchestrator.process_request("Hello world")
    
    assert response is not None
    assert response.summary == "Unified response generated successfully."
    assert len(response.detailed_sections) == 0 # no capabilities requested
