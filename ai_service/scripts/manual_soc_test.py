import asyncio
import json
import logging
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from app.agents.registry.factory import AgentFactory
from app.agents.manifests.loader import ManifestLoader
from app.agents.soc_analyst import SOCAnalystAgent
from app.agents.context import AgentContext, ExecutionContext, UserContext, ConversationContext, RuntimeContext
from app.llm.base import BaseLLMProvider
from app.llm.schemas import LLMRequest, LLMResponse

logging.basicConfig(level=logging.ERROR)

class MockLLM(BaseLLMProvider):
    async def generate(self, request: LLMRequest) -> LLMResponse:
        prompt_lower = request.prompt.lower()
        response_data = {
            "summary": "Mocked SOC summary.",
            "severity": "HIGH",
            "confidence": 0.9,
            "analysis": "Analyzed: " + request.prompt[:50],
            "mitre_mapping": ["T1059", "T1078"],
            "evidence": ["Log entry 4625", "IP 192.168.1.100"],
            "investigation_steps": ["Check related IP traffic"],
            "containment_recommendations": ["Block IP on firewall"],
            "detection_recommendations": ["Tune EDR alerts"],
            "references": [],
            "warnings": []
        }
        
        # Test 1: Handle malformed
        if "malformed" in prompt_lower:
            return LLMResponse(text="this is not JSON at all! crash test.", provider="mock", model="gpt-4", latency_ms=10)
            
        return LLMResponse(text=json.dumps(response_data), provider="mock", model="gpt-4", latency_ms=10)
        
    async def stream_generate(self, request): pass
    async def health_check(self): return {}

class MockRuntimeManager:
    def __init__(self):
        self.llm_provider = MockLLM()

async def main():
    print("Loading Manifest...")
    manifest = ManifestLoader.load_from_file("app/agents/manifests/files/soc_analyst.yaml")
    
    AgentFactory.register_agent_class("SOC Analyst", SOCAnalystAgent)
    agent = AgentFactory.create_agent(manifest)
    
    print(f"Instantiated Agent: {agent.manifest.name}\n")
    
    ctx = AgentContext(
        execution=ExecutionContext(execution_id="exec-123"),
        user=UserContext(user_id="user-123"),
        conversation=ConversationContext(session_id="session-123"),
        runtime=RuntimeContext()
    )
    # Patch runtime manager dynamically
    ctx.runtime.runtime_manager = MockRuntimeManager()
    
    print("--- Test 1: Standard SOC Analysis (Event 4625) ---")
    ctx.knowledge.retrieved_documents = [{"alert": "Event ID 4625 - Failed Logon from 192.168.1.100"}]
    res = await agent.execute(ctx)
    print(f"Success: {res.success}")
    print(f"Response snippet: {res.response[:200]}...\n")
    
    print("--- Test 2: Malformed Fallback Handling ---")
    ctx.knowledge.retrieved_documents = [{"alert": "malformed data test"}]
    res2 = await agent.execute(ctx)
    print(f"Response: {res2.response}")

if __name__ == "__main__":
    asyncio.run(main())
