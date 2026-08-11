from pydantic import BaseModel
from typing import Dict, Any, Optional, Union

class MCPError(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[MCPError] = None
    
    @property
    def is_error(self) -> bool:
        return self.error is not None
