from typing import Dict, Type
from app.chat.interfaces.i_execution_engine import IExecutionEngine
from app.chat.exceptions.chat_exceptions import EngineUnavailable

class ExecutionEngineRegistry:
    """
    Central registry where engines (RAG, Tool, General) register themselves at boot.
    Prevents the Orchestrator from hardcoding routing branches.
    """
    def __init__(self):
        self._engines: Dict[str, Type[IExecutionEngine]] = {}

    def register(self, name: str, engine_class: Type[IExecutionEngine]) -> None:
        """Register a new execution engine."""
        self._engines[name.upper()] = engine_class

    def get_engine_class(self, name: str) -> Type[IExecutionEngine]:
        """Retrieve an engine class by name."""
        engine = self._engines.get(name.upper())
        if not engine:
            raise EngineUnavailable(f"Execution Engine '{name}' is not registered.")
        return engine


class ExecutionEngineFactory:
    """
    Instantiates transient ExecutionEngines per request using the Registry.
    """
    def __init__(self, registry: ExecutionEngineRegistry):
        self._registry = registry

    def create_engine(self, name: str, **kwargs) -> IExecutionEngine:
        """
        Instantiate the requested engine, passing any necessary dependencies via kwargs.
        Wraps the engine in a RuntimePolicyProxy to ensure resilient execution.
        """
        from app.chat.policies.runtime_policy import RuntimePolicyProxy
        
        engine_class = self._registry.get_engine_class(name)
        # In a real DI framework (like DependencyInjector or FastAPI Depends), 
        # dependencies would be resolved automatically here.
        engine = engine_class(**kwargs)
        return RuntimePolicyProxy(engine)
