import threading
import logging
import json
from typing import List, Tuple, Dict, Any
from pathlib import Path
import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

from app.core.config import settings
from app.vector_store.base import BaseVectorStore
from app.vector_store.exceptions import IndexNotInitializedException, VectorStoreException

logger = logging.getLogger("app.vector_store.faiss")

class FaissVectorStore(BaseVectorStore):
    """
    FAISS provider managing the pure vector space operations.
    Defaults to IndexFlatIP (Inner Product) since embeddings are normalized.
    """
    def __init__(self):
        self.index = None
        self.dimension = None
        self.index_type = getattr(settings, "VECTOR_INDEX_TYPE", "IndexFlatIP")
        self.filepath = Path(getattr(settings, "VECTOR_PATH", "./vector_store/index.faiss"))
        self._lock = threading.Lock()
        
        # FAISS utilizes int64 IDs. We map our string Chunk IDs to ints.
        self.id_map: Dict[int, str] = {}
        self.rev_id_map: Dict[str, int] = {}
        self.next_int_id = 0

    def initialize(self, dimension: int) -> None:
        if faiss is None:
            raise VectorStoreException("faiss library is not installed.")
            
        with self._lock:
            self.dimension = dimension
            # IndexFlatIP is perfect for normalized cosine similarity
            if self.index_type == "IndexFlatIP":
                self.index = faiss.IndexIDMap(faiss.IndexFlatIP(dimension))
            else:
                self.index = faiss.IndexIDMap(faiss.IndexFlatL2(dimension))
            self.id_map.clear()
            self.rev_id_map.clear()
            self.next_int_id = 0
            logger.info(f"FAISS index initialized. Type: {self.index_type}, Dim: {self.dimension}")

    def load(self) -> None:
        with self._lock:
            if self.filepath.exists():
                self.index = faiss.read_index(str(self.filepath))
                self.dimension = self.index.d
                
                # Load the string-to-int mappings
                map_path = self.filepath.with_suffix(".map.json")
                if map_path.exists():
                    with open(map_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.id_map = {int(k): v for k, v in data.get("id_map", {}).items()}
                        self.rev_id_map = data.get("rev_id_map", {})
                        self.next_int_id = data.get("next_int_id", 0)

    def save(self) -> None:
        with self._lock:
            if self.index is None:
                return
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(self.filepath))
            
            map_path = self.filepath.with_suffix(".map.json")
            with open(map_path, "w", encoding="utf-8") as f:
                json.dump({
                    "id_map": self.id_map,
                    "rev_id_map": self.rev_id_map,
                    "next_int_id": self.next_int_id
                }, f)

    def _get_next_ids(self, count: int) -> List[int]:
        ids = list(range(self.next_int_id, self.next_int_id + count))
        self.next_int_id += count
        return ids

    def add(self, id: str, vector: List[float]) -> None:
        self.add_batch([id], [vector])

    def add_batch(self, ids: List[str], vectors: List[List[float]]) -> None:
        if self.index is None:
            raise IndexNotInitializedException("FAISS index not initialized.")
            
        with self._lock:
            np_vectors = np.array(vectors, dtype=np.float32)
            int_ids = self._get_next_ids(len(ids))
            np_ids = np.array(int_ids, dtype=np.int64)
            
            self.index.add_with_ids(np_vectors, np_ids)
            
            for int_id, str_id in zip(int_ids, ids):
                self.id_map[int_id] = str_id
                self.rev_id_map[str_id] = int_id

    def update(self, id: str, vector: List[float]) -> None:
        self.delete(id)
        self.add(id, vector)

    def delete(self, id: str) -> None:
        if self.index is None:
            return
        with self._lock:
            int_id = self.rev_id_map.get(id)
            if int_id is not None:
                self.index.remove_ids(np.array([int_id], dtype=np.int64))
                del self.id_map[int_id]
                del self.rev_id_map[id]

    def search(self, query_vector: List[float], top_k: int) -> Tuple[List[str], List[float]]:
        if self.index is None:
            raise IndexNotInitializedException("FAISS index not initialized.")
            
        np_query = np.array([query_vector], dtype=np.float32)
        scores, I = self.index.search(np_query, top_k)
        
        str_ids = []
        valid_scores = []
        for score, int_id in zip(scores[0], I[0]):
            if int_id != -1:
                str_ids.append(self.id_map.get(int_id))
                valid_scores.append(float(score))
                
        return str_ids, valid_scores

    def count(self) -> int:
        return self.index.ntotal if self.index else 0

    def health_check(self) -> Dict[str, Any]:
        return {
            "provider": "faiss",
            "index_type": self.index_type,
            "dimension": self.dimension,
            "vector_count": self.count(),
            "loaded": self.index is not None
        }
