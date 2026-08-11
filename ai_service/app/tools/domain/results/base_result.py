from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseResult(BaseModel):
    """
    Abstract base result for all tool outputs.
    Ensures outputs are typed and safe for serialization.
    """
    message: Optional[str] = None
    
    model_config = ConfigDict(
        frozen=True,
        extra="ignore"
    )
