import time
import uuid
import logging
from typing import Callable, Awaitable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import request_id_var

logger = logging.getLogger("app.middleware")

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle request logging and correlation ID generation.
    Logs HTTP method, path, status code, response time, client IP, and User Agent.
    """
    
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        request.state.request_id = correlation_id
        
        # Set context variable for logs
        request_id_var.set(correlation_id)
        
        start_time = time.time()
        
        client_ip = request.client.host if request.client else "Unknown"
        user_agent = request.headers.get("user-agent", "Unknown")
        method = request.method
        path = request.url.path

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            status_code = response.status_code
            
            logger.info(
                f"{method} {path} - Status {status_code} - Time {process_time:.2f} ms "
                f"- IP: {client_ip} - Agent: {user_agent}"
            )
            return response
        except Exception as exc:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"{method} {path} - FAILED - Time {process_time:.2f} ms "
                f"- IP: {client_ip} - Agent: {user_agent}"
            )
            raise exc
