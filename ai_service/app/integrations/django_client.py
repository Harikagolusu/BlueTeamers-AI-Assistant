import logging
import asyncio
import time
from typing import Optional, Dict, Any
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

logger = logging.getLogger("app.integrations.django_client")

class DjangoClient:
    """
    Reusable asynchronous client for communicating with the Django REST backend.
    Handles connection pooling, timeouts, automatic JWT injection, and retry policies.
    """
    def __init__(self):
        base_url = settings.DJANGO_API_URL
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        # Production-safe connection limits
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        # Timeouts: connect, read, write, pool
        timeout = httpx.Timeout(10.0, connect=5.0, read=30.0, write=10.0)
        self.client = httpx.AsyncClient(base_url=self.base_url, limits=limits, timeout=timeout)

    async def close(self):
        """Gracefully close the underlying httpx AsyncClient connections."""
        await self.client.aclose()

    async def _request(self, method: str, path: str, token: str, retries: int = 3, **kwargs) -> Any:
        url = path.lstrip("/")
        headers = kwargs.pop("headers", {})
        
        # Automatically forward the JWT token if provided
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        # Forward correlation ID for distributed tracing
        req_id = request_id_var.get()
        headers["X-Request-ID"] = req_id
        
        attempt = 0
        while attempt <= retries:
            start_time = time.time()
            try:
                response = await self.client.request(method, url, headers=headers, **kwargs)
                duration_ms = (time.time() - start_time) * 1000
                status = response.status_code
                
                logger.info(
                    f"DjangoClient: {method} {path} - Status {status} - Time {duration_ms:.2f} ms "
                    f"- ReqID: {req_id}"
                )
                
                # Check retriable status codes
                if status in (502, 503, 504) and attempt < retries:
                    attempt += 1
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                    
                # Handle non-retriable application errors
                if status in (401, 403):
                    raise UnauthorizedException(f"Django API unauthorized (Status {status}).")
                elif status == 404:
                    raise NotFoundException(f"Resource not found: {path}")
                elif status in (400, 422):
                    raise ValidationException(f"Validation error: {response.text}")
                
                # Raise for any other unexpected 4xx/5xx errors
                response.raise_for_status()
                
                # Return parsed JSON (assumes Django returns JSON for these endpoints)
                return response.json()
                
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError) as e:
                duration_ms = (time.time() - start_time) * 1000
                logger.warning(
                    f"DjangoClient Connection Error: {method} {path} - Time {duration_ms:.2f} ms "
                    f"- ReqID: {req_id} - Error: {str(e)}"
                )
                if attempt < retries:
                    attempt += 1
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise DjangoUnavailableException(f"Django API unavailable: {str(e)}")
            except httpx.HTTPStatusError as e:
                # Caught if raise_for_status triggers on an unhandled code
                logger.error(f"Django API HTTP error: {e.response.status_code} - {e.response.text}")
                raise DjangoAPIException(f"Django API returned error: {e.response.status_code}")
                
        raise DjangoUnavailableException("Max retries exceeded for Django API.")

    async def get(self, path: str, token: str, **kwargs) -> Any:
        return await self._request("GET", path, token, **kwargs)

    async def post(self, path: str, token: str, **kwargs) -> Any:
        return await self._request("POST", path, token, **kwargs)

    async def put(self, path: str, token: str, **kwargs) -> Any:
        return await self._request("PUT", path, token, **kwargs)

    async def patch(self, path: str, token: str, **kwargs) -> Any:
        return await self._request("PATCH", path, token, **kwargs)

    async def delete(self, path: str, token: str, **kwargs) -> Any:
        return await self._request("DELETE", path, token, **kwargs)

# Singleton instance for dependency injection
django_client = DjangoClient()
