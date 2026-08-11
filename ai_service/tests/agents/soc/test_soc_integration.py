import pytest
import os
from app.agents.soc_analyst import SOCAnalystAgent
from app.agents.manifests.loader import ManifestLoader
from app.tools.implementations.cybersecurity.mitre_tool import MITRETool
from app.tools.context import ToolContext

@pytest.fixture
def agent():
    manifest_path = os.path.join(os.path.dirname(__file__), "../../../app/agents/manifests/files/soc_analyst.yaml")
    manifest = ManifestLoader.load_from_file(manifest_path)
    return SOCAnalystAgent(manifest)

@pytest.mark.asyncio
async def test_tool_integration_execution(agent):
    tool = MITRETool()
    tool_ctx = ToolContext()
    
    result = await tool.execute(tool_ctx, technique_id="T1059")
    
    assert "tactic" in result
    assert result["tactic"] == "Execution"
