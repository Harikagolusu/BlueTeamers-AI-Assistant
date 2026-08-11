from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """
    Abstract base schema for all tool inputs.
    Enforces strict validation rules across the domain.
    """
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        validate_assignment=True,
        strict=True
    )
