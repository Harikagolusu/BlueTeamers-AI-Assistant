from typing import Dict, Any

class PlatformAgentOrchestratorManifest:
    name = "PlatformAgentOrchestrator"
    version = "2.0.0"
    description = "Central coordination layer of the BlueTeamers AI Assistant platform."
    capabilities = [
        "INTENT_ANALYSIS",
        "CAPABILITY_RESOLUTION",
        "EXECUTION_PLANNING",
        "WORKFLOW_SCHEDULING",
        "AGENT_INVOCATION",
        "RESPONSE_AGGREGATION",
        "FAILURE_RECOVERY",
        "CONTEXT_MANAGEMENT"
    ]
    
    @classmethod
    def get_metadata(cls) -> Dict[str, Any]:
        return {
            "name": cls.name,
            "version": cls.version,
            "description": cls.description,
            "capabilities": cls.capabilities
        }
