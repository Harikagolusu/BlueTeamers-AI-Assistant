from typing import Protocol, List, Optional, Any
from pydantic import BaseModel

class ExecutionHistoryRecord(BaseModel):
    workflow_id: str
    request_id: str
    status: str
    result: Any
    created_at: str

class ExecutionHistoryRepository(Protocol):
    def save(self, record: ExecutionHistoryRecord) -> None:
        ...
    def get(self, workflow_id: str) -> Optional[ExecutionHistoryRecord]:
        ...
    def list(self) -> List[ExecutionHistoryRecord]:
        ...
    def delete(self, workflow_id: str) -> None:
        ...

class InMemoryExecutionHistoryRepository:
    def __init__(self):
        self._store = {}
        
    def save(self, record: ExecutionHistoryRecord) -> None:
        self._store[record.workflow_id] = record
        
    def get(self, workflow_id: str) -> Optional[ExecutionHistoryRecord]:
        return self._store.get(workflow_id)
        
    def list(self) -> List[ExecutionHistoryRecord]:
        return list(self._store.values())
        
    def delete(self, workflow_id: str) -> None:
        if workflow_id in self._store:
            del self._store[workflow_id]
