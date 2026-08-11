from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class ExecutionMetrics(BaseModel):
    steps_executed: int = 0
    retry_count: int = 0
    skipped_steps: int = 0
    failed_steps: int = 0
    recovery_count: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def execution_duration_ms(self) -> float:
        if not self.start_time or not self.end_time:
            return 0.0
        return (self.end_time - self.start_time).total_seconds() * 1000

class JournalEntry(BaseModel):
    entry_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ExecutionJournal(BaseModel):
    """Immutable authoritative record of execution."""
    journal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metrics: ExecutionMetrics = Field(default_factory=ExecutionMetrics)
    entries: List[JournalEntry] = Field(default_factory=list)

    def record(self, event_type: str, details: Dict[str, Any] = None):
        entry = JournalEntry(
            event_type=event_type,
            details=details or {}
        )
        self.entries.append(entry)
