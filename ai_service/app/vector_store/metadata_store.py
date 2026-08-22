import json
import threading
from pathlib import Path
from typing import Dict, Any, Optional

from app.core.config import settings

class MetadataStore:
    """
    Persists and manages metadata entirely separately from FAISS.
    FAISS is highly optimized for floats; shoving string metadata inside it degrades performance.
    """
    def __init__(self):
        # We read config at init to allow mocking/tests to override settings easily
        path_str = getattr(settings, "VECTOR_METADATA_FILE", "./vector_store/metadata.json")
        self.filepath = Path(path_str)
        self.metadata: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def save(self) -> None:
        with self._lock:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f)

    def load(self) -> None:
        with self._lock:
            if self.filepath.exists():
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {}

    def update(self, id: str, metadata: Dict[str, Any]) -> None:
        with self._lock:
            self.metadata[id] = metadata

    def delete(self, id: str) -> None:
        with self._lock:
            self.metadata.pop(id, None)

    def get(self, id: str) -> Optional[Dict[str, Any]]:
        return self.metadata.get(id)

    def count(self) -> int:
        return len(self.metadata)
