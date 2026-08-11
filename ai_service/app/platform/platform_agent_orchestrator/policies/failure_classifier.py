from enum import Enum
from pydantic import BaseModel
from typing import Optional

class FailureCategory(str, Enum):
    AGENT_UNAVAILABLE = "AgentUnavailable"
    CAPABILITY_UNAVAILABLE = "CapabilityUnavailable"
    TIMEOUT = "Timeout"
    VALIDATION_ERROR = "ValidationError"
    EXECUTION_ERROR = "ExecutionError"
    PARTIAL_SUCCESS = "PartialSuccess"
    INTERNAL_FAILURE = "InternalFailure"

class FailureClassifier:
    @staticmethod
    def classify(error: Exception) -> FailureCategory:
        # Mock logic to classify errors
        err_str = str(error).lower()
        if "timeout" in err_str:
            return FailureCategory.TIMEOUT
        if "capability" in err_str:
            return FailureCategory.CAPABILITY_UNAVAILABLE
        if "unavailable" in err_str:
            return FailureCategory.AGENT_UNAVAILABLE
        if "validation" in err_str:
            return FailureCategory.VALIDATION_ERROR
        return FailureCategory.EXECUTION_ERROR
