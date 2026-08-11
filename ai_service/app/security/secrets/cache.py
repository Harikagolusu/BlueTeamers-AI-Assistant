from typing import Dict
from datetime import datetime, timedelta, timezone

class SecretCache:
    def __init__(self, ttl_minutes: int = 15):
        self._cache: Dict[str, dict] = {}
        self._ttl = ttl_minutes

    def get(self, secret_id: str) -> str:
        if secret_id in self._cache:
            entry = self._cache[secret_id]
            if datetime.now(timezone.utc) < entry["expires"]:
                return entry["value"]
            del self._cache[secret_id]
        return None

    def put(self, secret_id: str, value: str) -> None:
        self._cache[secret_id] = {
            "value": value,
            "expires": datetime.now(timezone.utc) + timedelta(minutes=self._ttl)
        }

    def invalidate(self, secret_id: str) -> None:
        if secret_id in self._cache:
            del self._cache[secret_id]
