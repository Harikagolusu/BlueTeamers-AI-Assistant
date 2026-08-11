import time
import json
import logging
import httpx
from typing import AsyncGenerator, Dict, Any
from fastapi import status

from app.core.config import settings
from app.core.logging import request_id_var
from app.llm.base import BaseLLMProvider
from app.llm.schemas import LLMRequest, LLMResponse
from app.llm.exceptions import (
    ProviderUnavailableException,
    ModelNotFoundException,
    LLMTimeoutException,
    LLMException,
    ProviderConfigurationException
)

logger = logging.getLogger("app.llm.omniroute")

class OmniRouteProvider(BaseLLMProvider):
    """OmniRoute implementation using OpenAI-compatible chat completions API."""
    
    def __init__(self):
        if not settings.OMNIROUTE_API_KEY:
            raise ProviderConfigurationException("OMNIROUTE_API_KEY is required when using OmniRoute provider")

        self.base_url = (settings.OMNIROUTE_BASE_URL or "").rstrip('/')
        self.model = settings.OMNIROUTE_MODEL
        
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        timeout = httpx.Timeout(120.0, connect=5.0)
        headers = {
            "Authorization": f"Bearer {settings.OMNIROUTE_API_KEY}",
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=headers, limits=limits, timeout=timeout)
        self.provider_name = "omniroute"

    async def close(self):
        await self.client.aclose()

    def _build_messages(self, request: LLMRequest) -> list:
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        return messages

    async def generate(self, request: LLMRequest) -> LLMResponse:
        start_time = time.time()
        req_id = request_id_var.get()
        
        payload = {
            "model": self.model,
            "messages": self._build_messages(request),
            "stream": False,
            "temperature": request.temperature
        }

        try:
            logger.info(f"LLM Request - Provider: {self.provider_name} - Model: {self.model} - ReqID: {req_id}")
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()
            
            data = response.json()
            latency = (time.time() - start_time) * 1000
            
            logger.info(f"LLM Response - Provider: {self.provider_name} - Model: {self.model} - Latency: {latency:.2f} ms - ReqID: {req_id}")
            
            text = ""
            choices = data.get("choices", [])
            if choices and len(choices) > 0:
                text = choices[0].get("message", {}).get("content", "")
            
            usage = data.get("usage", {})
                
            return LLMResponse(
                text=text,
                provider=self.provider_name,
                model=self.model,
                latency_ms=latency,
                finish_reason=choices[0].get("finish_reason", "stop") if choices else "stop",
                usage={
                    "prompt_eval_count": usage.get("prompt_tokens", 0),
                    "eval_count": usage.get("completion_tokens", 0)
                }
            )
            
        except httpx.ReadTimeout:
            logger.error(f"LLM Timeout - Provider: {self.provider_name} - ReqID: {req_id}")
            raise LLMTimeoutException("OmniRoute generation timed out")
        except httpx.ConnectError:
            logger.error(f"LLM Connection Error - Provider: {self.provider_name} - ReqID: {req_id}")
            raise ProviderUnavailableException("OmniRoute API is unreachable")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                logger.error(f"LLM Model Not Found - Model: {self.model} - ReqID: {req_id}")
                raise ModelNotFoundException(f"OmniRoute model '{self.model}' not found")
            elif e.response.status_code == status.HTTP_401_UNAUTHORIZED:
                logger.error(f"LLM Unauthorized Error - Invalid API Key - ReqID: {req_id}")
                raise LLMException("OmniRoute authentication failed. Invalid API Key.")
            logger.error(f"LLM HTTP Error - Status: {e.response.status_code} - ReqID: {req_id}")
            raise LLMException(f"OmniRoute returned error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"LLM Unexpected Error - ReqID: {req_id} - Error: {str(e)}")
            raise LLMException(f"Unexpected error in OmniRoute provider: {str(e)}")

    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        req_id = request_id_var.get()
        payload = {
            "model": self.model,
            "messages": self._build_messages(request),
            "stream": True,
            "temperature": request.temperature
        }
            
        logger.info(f"LLM Stream Request - Provider: {self.provider_name} - Model: {self.model} - ReqID: {req_id}")

        try:
            async with self.client.stream("POST", "/chat/completions", json=payload) as response:
                response.raise_for_status()
                async for chunk in response.aiter_lines():
                    if chunk.startswith("data: "):
                        data_str = chunk[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            choices = data.get("choices", [])
                            if choices and len(choices) > 0:
                                delta = choices[0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
        except httpx.ReadTimeout:
            raise LLMTimeoutException("OmniRoute streaming timed out")
        except httpx.ConnectError:
            raise ProviderUnavailableException("OmniRoute API is unreachable")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_401_UNAUTHORIZED:
                raise LLMException("OmniRoute authentication failed. Invalid API Key.")
            raise LLMException(f"OmniRoute returned error: {e.response.status_code}")
        except Exception as e:
            raise LLMException(f"Streaming failed: {str(e)}")

    async def health_check(self) -> Dict[str, Any]:
        start_time = time.time()
        healthy = False
        try:
            # We can use /models to check if the API is reachable and key is valid.
            # Bound the probe so a slow gateway can't stall the health endpoint.
            response = await self.client.get("/models", timeout=httpx.Timeout(10.0, connect=5.0))
            if response.status_code == 200:
                healthy = True
        except Exception:
            pass

        latency = (time.time() - start_time) * 1000
        return {
            "provider": self.provider_name,
            "model": self.model,
            "healthy": healthy,
            "status": "healthy" if healthy else "unhealthy",
            "latency_ms": latency
        }
