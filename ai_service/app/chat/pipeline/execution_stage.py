from app.chat.interfaces.i_execution_stage import IExecutionStage
from app.chat.context.execution_context import ExecutionContext
from app.chat.engines.registry import ExecutionEngineFactory
from app.chat.exceptions.chat_exceptions import RoutingError

class EngineExecutionStage(IExecutionStage):
    """Instantiates the selected engine and executes it."""
    
    def __init__(self, engine_factory: ExecutionEngineFactory):
        self._engine_factory = engine_factory

    @property
    def name(self) -> str:
        return "Execution"

    async def execute(self, context: ExecutionContext) -> ExecutionContext:
        if "execution_result" in context.metadata:
            return context
            
        engine_name = context.metadata.get("selected_engine")
        if not engine_name:
            raise RoutingError("No execution engine was selected by the planner.")
            
        engine = self._engine_factory.create_engine(engine_name)
        result = await engine.execute(context)
        
        # Storing the ExecutionResult inside the context metadata for the next stage
        new_metadata = {**context.metadata, "execution_result": result}
        return context.model_copy(update={"metadata": new_metadata})
