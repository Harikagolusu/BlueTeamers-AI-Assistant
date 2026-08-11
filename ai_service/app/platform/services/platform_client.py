import logging
import asyncio
import time
from typing import Optional, Dict, Any, Tuple
import httpx

from app.core.config import settings
from app.core.exceptions import (
    DjangoAPIException,
    DjangoUnavailableException,
    UnauthorizedException,
    NotFoundException,
    ValidationException
)
from app.core.logging import request_id_var

logger = logging.getLogger("app.platform.services.platform_client")

class PlatformApiClient:
    """
    Client for communicating with the Django REST backend.
    Includes connection pooling, retries, JWT injection, and TTL caching.
    """
    def __init__(self, cache_ttl_seconds: int = 60):
        self.base_url = settings.DJANGO_API_URL
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        timeout = httpx.Timeout(10.0, connect=5.0, read=30.0, write=10.0)
        self.client = httpx.AsyncClient(base_url=self.base_url, limits=limits, timeout=timeout)
        self.cache_ttl = cache_ttl_seconds
        # Simple TTL cache: key -> (timestamp, data)
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self._lock = asyncio.Lock()

    async def close(self):
        await self.client.aclose()

    async def _get_cached(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key in self._cache:
                timestamp, data = self._cache[key]
                if time.time() - timestamp < self.cache_ttl:
                    return data
                else:
                    del self._cache[key]
        return None

    async def _set_cache(self, key: str, data: Any):
        async with self._lock:
            self._cache[key] = (time.time(), data)

    async def _request(self, method: str, path: str, token: str, retries: int = 3, **kwargs) -> Any:
        url = path
        headers = kwargs.pop("headers", {})
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/json"
        
        req_id = request_id_var.get()
        if req_id:
            headers["X-Request-ID"] = req_id
        
        # Cache logic for GET requests
        cache_key = f"{method}:{path}:{token}"
        if method == "GET":
            cached_data = await self._get_cached(cache_key)
            if cached_data is not None:
                logger.debug(f"Cache hit for {path}")
                return cached_data

        attempt = 0
        while attempt <= retries:
            start_time = time.time()
            try:
                response = await self.client.request(method, url, headers=headers, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                status = response.status_code
                
                logger.info(
                    f"{method} {response.url}\n{status} OK\nResponse Time: {duration_ms:.2f} ms"
                )
                
                if status in (502, 503, 504) and attempt < retries:
                    attempt += 1
                    await asyncio.sleep(2 ** attempt)
                    continue
                    
                if status in (401, 403):
                    raise UnauthorizedException(f"Django API unauthorized (Status {status}).")
                elif status == 404:
                    raise NotFoundException(f"Resource not found: {path}")
                elif status in (400, 422):
                    raise ValidationException(f"Validation error: {response.text}")
                
                response.raise_for_status()
                data = response.json()
                
                if method == "GET":
                    await self._set_cache(cache_key, data)
                    
                return data
                
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError) as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.warning(
                    f"PlatformApiClient Connection Error: {method} {path} - Time {duration_ms:.2f} ms - Error: {str(e)}"
                )
                if attempt < retries:
                    attempt += 1
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise DjangoUnavailableException(f"Django API unavailable: {str(e)}")
            except httpx.HTTPStatusError as e:
                logger.error(f"Django API HTTP error: {e.response.status_code} - {e.response.text}")
                raise DjangoAPIException(f"Django API returned error: {e.response.status_code}")
                
        raise DjangoUnavailableException("Max retries exceeded for Django API.")

    async def get(self, path: str, token: str, **kwargs) -> Any:
        return await self._request("GET", path, token, **kwargs)

    async def post(self, path: str, token: str, **kwargs) -> Any:
        return await self._request("POST", path, token, **kwargs)

platform_client = PlatformApiClient()
