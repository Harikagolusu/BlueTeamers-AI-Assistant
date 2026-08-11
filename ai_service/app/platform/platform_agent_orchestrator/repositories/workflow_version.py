from typing import Protocol, List, Optional
from pydantic import BaseModel

class WorkflowVersion(BaseModel):
    version: str
    created_at: str
    author: str
    change_reason: str
    compatibility: List[str]

class WorkflowVersionRepository(Protocol):
    def save(self, wf_version: WorkflowVersion) -> None:
        ...
    def get(self, version: str) -> Optional[WorkflowVersion]:
        ...
    def list(self) -> List[WorkflowVersion]:
        ...

class InMemoryWorkflowVersionRepository:
    def __init__(self):
        self._store = {}
        
    def save(self, wf_version: WorkflowVersion) -> None:
        self._store[wf_version.version] = wf_version
        
    def get(self, version: str) -> Optional[WorkflowVersion]:
        return self._store.get(version)
        
    def list(self) -> List[WorkflowVersion]:
        return list(self._store.values())
