import logging
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from app.guardrails.dependencies import get_guardrails_service
from app.guardrails.domain.models.context import GuardrailContext
from app.guardrails.exceptions.guardrail_exceptions import GuardrailException, PolicyViolationError
import uuid

logger = logging.getLogger(__name__)

class GuardrailsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Only run guardrails for specific endpoints, e.g., /chat or /rag
        # Skip streaming endpoints as they bypass middleware (per streaming consideration)
        if not (request.url.path.startswith("/api/v1/chat") or request.url.path.startswith("/api/v1/rag")):
            return await call_next(request)
            
        if request.url.path.endswith("/stream"):
            return await call_next(request)

        try:
            # Extract request body
            body_bytes = await request.body()
            text = ""
            
            if body_bytes:
                try:
                    body_json = json.loads(body_bytes)
                    text = body_json.get("query") or body_json.get("text") or body_json.get("prompt") or ""
                except json.JSONDecodeError:
                    text = body_bytes.decode('utf-8', errors='ignore')

            # Reconstruct request body for downstream consumption
            async def receive():
                return {"type": "http.request", "body": body_bytes}
            request._receive = receive
            
            context = GuardrailContext(
                text=text,
                trace_id=request.headers.get("X-Trace-Id", str(uuid.uuid4())),
                request_id=str(uuid.uuid4()),
                client_application=request.headers.get("User-Agent")
            )
            
            service = get_guardrails_service()
            
            # Input Guardrails
            context = await service.validate_input(context)
            
            # Continue down the stack
            response = await call_next(request)
            
            # Output Guardrails
            # We intercept JSON responses to validate their output
            if response.status_code == 200 and response.headers.get("content-type") == "application/json":
                # Extract response body
                res_body = b""
                async for chunk in response.body_iterator:
                    res_body += chunk
                
                res_text = ""
                try:
                    res_json = json.loads(res_body)
                    res_text = res_json.get("answer") or res_json.get("text") or res_json.get("response") or ""
                except json.JSONDecodeError:
                    res_text = res_body.decode('utf-8', errors='ignore')
                    
                context.text = res_text
                context = await service.validate_output(context)
                
                # We need to return a new response because the original iterator is consumed
                return Response(
                    content=res_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type
                )
                
            return response
            
        except PolicyViolationError as e:
            logger.warning(f"Guardrail blocked request: {str(e)}")
            return JSONResponse(status_code=403, content={"detail": "Request blocked by security policy.", "reason": str(e)})
        except GuardrailException as e:
            logger.error(f"Guardrail internal error: {str(e)}")
            return JSONResponse(status_code=500, content={"detail": "Internal guardrail error."})
