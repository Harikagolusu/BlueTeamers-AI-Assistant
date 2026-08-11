from app.tools.base import BaseTool, ToolMetadata
from app.tools.context import ToolContext
from app.platform.platform_agent_orchestrator.repositories.execution_history import ExecutionHistoryRepository, ExecutionHistoryRecord
import datetime
from datetime import timezone
from typing import Any

class HistoryPersistenceTool(BaseTool):
    def __init__(self, history_repo: ExecutionHistoryRepository):
        super().__init__(
            name="history_persistence",
            metadata=ToolMetadata(
                input_schema={"workflow_id": "str", "request_id": "str", "status": "str", "result": "Any"},
                output_schema={"success": "bool"},
                tags=["orchestration", "persistence"]
            )
        )
        self.history_repo = history_repo

    async def execute(self, context: ToolContext, **kwargs) -> Any:
        workflow_id = kwargs.get("workflow_id")
        request_id = kwargs.get("request_id")
        status = kwargs.get("status")
        result = kwargs.get("result")
        
        record = ExecutionHistoryRecord(
            workflow_id=workflow_id,
            request_id=request_id,
            status=status,
            result=result,
            created_at=datetime.datetime.now(timezone.utc).isoformat()
        )
        
        self.history_repo.save(record)
        return True
