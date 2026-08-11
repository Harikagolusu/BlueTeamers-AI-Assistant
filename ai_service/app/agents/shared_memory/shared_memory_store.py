import json
import uuid
import threading
from typing import Any, Dict, Optional
from app.agents.interfaces.i_shared_memory import ISharedMemory

class SharedMemoryStore(ISharedMemory):
    """
    Explicitly modeled shared memory with namespaces for 
    Conversation Context, Intermediate Results, Shared Variables, Agent Notes, and Version History.
    """
    def __init__(self):
        self._namespaces: Dict[str, Dict[str, Any]] = {
            "conversation_context": {},
            "intermediate_results": {},
            "shared_variables": {},
            "agent_notes": {}
        }
        self._snapshots: Dict[str, str] = {}
        self._lock = threading.RLock()

    def read(self, key: str, namespace: str = "shared_variables") -> Optional[Any]:
        with self._lock:
            ns = self._namespaces.get(namespace)
            if ns is not None:
                return ns.get(key)
            return None

    def write(self, key: str, value: Any, namespace: str = "shared_variables") -> None:
        with self._lock:
            if namespace not in self._namespaces:
                self._namespaces[namespace] = {}
            self._namespaces[namespace][key] = value

    def get_namespace(self, namespace: str) -> Dict[str, Any]:
        with self._lock:
            # Return a shallow copy to prevent direct mutation without locks
            return dict(self._namespaces.get(namespace, {}))

    def create_snapshot(self) -> str:
        with self._lock:
            snapshot_id = str(uuid.uuid4())
            # Simple JSON serialization for snapshotting state
            self._snapshots[snapshot_id] = json.dumps(self._namespaces)
            return snapshot_id

    def restore_snapshot(self, snapshot_id: str) -> None:
        with self._lock:
            if snapshot_id in self._snapshots:
                self._namespaces = json.loads(self._snapshots[snapshot_id])
            else:
                raise ValueError(f"Snapshot {snapshot_id} not found.")
