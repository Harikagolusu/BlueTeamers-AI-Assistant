from app.planning.interfaces.i_engine_resolver import IExecutionEngineResolver
from app.planning.models.plan import Capability

class CapabilityEngineResolver(IExecutionEngineResolver):
    def __init__(self):
        # Maps abstract capability to the concrete string name of the engine registered in ExecutionEngineRegistry
        self._mapping = {
            Capability.LLM: "GENERAL",
            Capability.RAG: "RAG",
            Capability.TOOL: "TOOL",
            Capability.CLARIFICATION: "GENERAL", # fallback
            Capability.MEMORY: "GENERAL",
            Capability.SEARCH: "TOOL",
            Capability.REASONING: "GENERAL",
            Capability.KNOWLEDGE_ASSISTANT: "RAG",
            Capability.INVESTIGATION_AGENT: "TOOL",
            Capability.LEARNING_COACH: "GENERAL",
            Capability.AGGREGATOR: "GENERAL"
        }
        
    def resolve(self, capability: Capability) -> str:
        return self._mapping.get(capability, "GENERAL")
