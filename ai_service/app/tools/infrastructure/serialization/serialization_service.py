from enum import Enum
from uuid import UUID
from datetime import datetime
from typing import Any, Dict, List

class SerializationService:
    """
    Standardizes serialization across all tools.
    """
    @classmethod
    def serialize(cls, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, dict):
            return {k: cls.serialize(v) for k, v in obj.items()}
        if isinstance(obj, list) or isinstance(obj, tuple):
            return [cls.serialize(item) for item in obj]
        if hasattr(obj, "model_dump"): # Pydantic v2
            return cls.serialize(obj.model_dump())
        if hasattr(obj, "dict"): # Pydantic v1
            return cls.serialize(obj.dict())
        return obj
