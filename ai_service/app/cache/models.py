from pydantic import BaseModel

class CacheConfig(BaseModel):
    enabled: bool = False
    ttl_seconds: int = 3600
    max_size: int = 1000
    backend: str = "memory"
