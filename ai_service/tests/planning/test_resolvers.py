import pytest
from app.planning.models.plan import Capability
from app.planning.resolvers.engine_resolver import CapabilityEngineResolver

def test_engine_resolver():
    resolver = CapabilityEngineResolver()
    
    assert resolver.resolve(Capability.LLM) == "GENERAL"
    assert resolver.resolve(Capability.RAG) == "RAG"
    assert resolver.resolve(Capability.TOOL) == "TOOL"
    assert resolver.resolve(Capability.SEARCH) == "TOOL"
    assert resolver.resolve(Capability.CLARIFICATION) == "GENERAL"
    
    # Enum fallback test
    class DummyEnum:
        UNKNOWN = "UNKNOWN"
    assert resolver.resolve(DummyEnum.UNKNOWN) == "GENERAL"
