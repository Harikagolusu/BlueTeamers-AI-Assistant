from abc import abstractmethod
from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.tools.interfaces.i_tool import ITool
from app.tools.context import ToolContext

class ToolMetadata(BaseModel):
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    permissions: List[str] = Field(default_factory=list)
    timeout: int = 30
    cost: float = 0.0
    tags: List[str] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)

class BaseTool(ITool):
    """
    Base implementation of a Tool.
    Requires extending classes to define metadata and the async execute method.
    """
    def __init__(self, name: str, metadata: ToolMetadata):
        self._name = name
        self._metadata = metadata

    @property
    def name(self) -> str:
        return self._name

    @property
    def metadata(self) -> ToolMetadata:
        return self._metadata

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    @abstractmethod
    async def execute(self, context: ToolContext, **kwargs) -> Any:
        pass
