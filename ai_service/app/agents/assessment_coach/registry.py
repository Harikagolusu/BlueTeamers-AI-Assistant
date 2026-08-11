from app.agents.registry.agent_registry import AgentRegistry
from app.agents.assessment_coach.agent import AssessmentCoachAgent
import yaml
import os

def register_agent(registry: AgentRegistry):
    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.yaml")
    with open(manifest_path, "r") as f:
        manifest_data = yaml.safe_load(f)
        
    class MockManifest:
        pass
    
    manifest_obj = MockManifest()
    manifest_obj.capabilities = [
        "ASSESSMENT",
        "COMPETENCY_EVALUATION",
        "READINESS_ASSESSMENT",
        "ADAPTIVE_ASSESSMENT",
        "KNOWLEDGE_EVALUATION",
        "PRACTICAL_EVALUATION",
        "SCENARIO_EVALUATION"
    ]
        
    agent = AssessmentCoachAgent(manifest=manifest_obj)
    registry.register("assessment_coach", agent)
