from typing import Any, Type, TypeVar
from pydantic import BaseModel, ValidationError

T = TypeVar('T', bound=BaseModel)

class ValidationService:
    """
    Provides reusable validation logic.
    """
    @staticmethod
    def validate_schema(schema_class: Type[T], data: dict) -> T:
        try:
            return schema_class.model_validate(data)
        except ValidationError as e:
            raise ValueError(f"Schema validation failed: {e.errors()}")
