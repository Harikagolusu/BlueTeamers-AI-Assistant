import pytest
from app.chat.engines.registry import ExecutionEngineRegistry, ExecutionEngineFactory
from app.chat.engines.general_engine import GeneralExecutionEngine
from app.chat.engines.rag_engine import RagExecutionEngine
from app.chat.exceptions.chat_exceptions import EngineUnavailable

def test_registry_registration():
    registry = ExecutionEngineRegistry()
    registry.register("GENERAL", GeneralExecutionEngine)
    registry.register("RAG", RagExecutionEngine)
    
    assert registry.get_engine_class("GENERAL") == GeneralExecutionEngine
    assert registry.get_engine_class("RAG") == RagExecutionEngine

def test_registry_missing_engine():
    registry = ExecutionEngineRegistry()
    
    with pytest.raises(EngineUnavailable):
        registry.get_engine_class("MISSING")

def test_engine_factory():
    registry = ExecutionEngineRegistry()
    registry.register("GENERAL", GeneralExecutionEngine)
    
    factory = ExecutionEngineFactory(registry)
    from unittest.mock import AsyncMock, MagicMock
    mock_llm = AsyncMock()
    mock_prompt_builder = MagicMock()
    
    # Factory uses RuntimePolicyProxy
    from app.chat.policies.runtime_policy import RuntimePolicyProxy
    engine = factory.create_engine("GENERAL", llm_service=mock_llm, prompt_builder=mock_prompt_builder)
    
    assert isinstance(engine, RuntimePolicyProxy)
    assert engine.name == "GENERAL"
