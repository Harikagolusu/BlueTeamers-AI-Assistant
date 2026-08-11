from typing import Any
from app.tools.models.tool_response import ToolResponse
from app.tools.infrastructure.serialization.serialization_service import SerializationService

class ResponseBuilder:
    """
    Guarantees consistent responses across every tool.
    """
    @staticmethod
    def success(result: Any, metadata: dict = None) -> ToolResponse:
        return ToolResponse(
            success=True,
            result=SerializationService.serialize(result),
            error=None,
            metadata=metadata or {}
        )

    @staticmethod
    def failure(error_msg: str, metadata: dict = None) -> ToolResponse:
        return ToolResponse(
            success=False,
            result=None,
            error=error_msg,
            metadata=metadata or {}
        )

    @staticmethod
    def validation_error(error_msg: str, metadata: dict = None) -> ToolResponse:
        meta = metadata or {}
        meta["error_type"] = "validation_error"
        return ResponseBuilder.failure(error_msg, meta)

    @staticmethod
    def system_error(error_msg: str, metadata: dict = None) -> ToolResponse:
        meta = metadata or {}
        meta["error_type"] = "system_error"
        return ResponseBuilder.failure(error_msg, meta)

    @staticmethod
    def permission_error(error_msg: str, metadata: dict = None) -> ToolResponse:
        meta = metadata or {}
        meta["error_type"] = "permission_error"
        return ResponseBuilder.failure(error_msg, meta)

    @staticmethod
    def timeout_error(error_msg: str, metadata: dict = None) -> ToolResponse:
        meta = metadata or {}
        meta["error_type"] = "timeout_error"
        return ResponseBuilder.failure(error_msg, meta)
