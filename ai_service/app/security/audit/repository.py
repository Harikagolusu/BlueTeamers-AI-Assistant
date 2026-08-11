from typing import List, Dict, Any
from app.security.interfaces.i_audit import IAuditRepository
from app.security.models.audit_record import AuditRecord
import threading

class InMemoryAuditRepository(IAuditRepository):
    def __init__(self):
        self._records: List[AuditRecord] = []
        self._lock = threading.RLock()

    def save(self, record: AuditRecord) -> None:
        with self._lock:
            self._records.append(record)

    def query(self, filters: Dict[str, Any]) -> List[AuditRecord]:
        with self._lock:
            results = []
            for r in self._records:
                match = True
                for k, v in filters.items():
                    if getattr(r, k, None) != v:
                        match = False
                        break
                if match:
                    results.append(r)
            return results
