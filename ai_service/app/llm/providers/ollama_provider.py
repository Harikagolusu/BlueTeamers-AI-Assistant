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
    LLMException
)

logger = logging.getLogger("app.llm.ollama")

class OllamaProvider(BaseLLMProvider):
    """Ollama implementation for local development and edge deployment."""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL or "http://localhost:11434"
        self.model = settings.OLLAMA_MODEL
        
        # Optimize connection limits for internal network latency
        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        timeout = httpx.Timeout(120.0, connect=5.0)
        self.client = httpx.AsyncClient(base_url=self.base_url, limits=limits, timeout=timeout)
        self.provider_name = "ollama"

    async def close(self):
        await self.client.aclose()

    async def generate(self, request: LLMRequest) -> LLMResponse:
        start_time = time.time()
        req_id = request_id_var.get()
        
        payload = {
            "model": self.model,
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature
            }
        }
        if request.system_prompt:
            payload["system"] = request.system_prompt

        try:
            logger.info(f"LLM Request - Provider: {self.provider_name} - Model: {self.model} - ReqID: {req_id}")
            response = await self.client.post("/api/generate", json=payload)
            response.raise_for_status()
            
            data = response.json()
            latency = (time.time() - start_time) * 1000
            
            logger.info(f"LLM Response - Provider: {self.provider_name} - Model: {self.model} - Latency: {latency:.2f} ms - ReqID: {req_id}")
            
            return LLMResponse(
                text=data.get("response", ""),
                provider=self.provider_name,
                model=self.model,
                latency_ms=latency,
                finish_reason="stop",
                usage={
                    "prompt_eval_count": data.get("prompt_eval_count", 0),
                    "eval_count": data.get("eval_count", 0)
                }
            )
            
        except httpx.ReadTimeout:
            logger.error(f"LLM Timeout - Provider: {self.provider_name} - ReqID: {req_id}")
            raise LLMTimeoutException("Ollama generation timed out")
        except httpx.ConnectError:
            logger.error(f"LLM Connection Error - Provider: {self.provider_name} - ReqID: {req_id}")
            raise ProviderUnavailableException("Ollama API is unreachable")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == status.HTTP_404_NOT_FOUND:
                logger.error(f"LLM Model Not Found - Model: {self.model} - ReqID: {req_id}")
                raise ModelNotFoundException(f"Ollama model '{self.model}' not found")
            logger.error(f"LLM HTTP Error - Status: {e.response.status_code} - ReqID: {req_id}")
            raise LLMException(f"Ollama returned error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"LLM Unexpected Error - ReqID: {req_id} - Error: {str(e)}")
            raise LLMException(f"Unexpected error in Ollama provider: {str(e)}")

    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        req_id = request_id_var.get()
        payload = {
            "model": self.model,
            "prompt": request.prompt,
            "stream": True,
            "options": {
                "temperature": request.temperature
            }
        }
        if request.system_prompt:
            payload["system"] = request.system_prompt
            
        logger.info(f"LLM Stream Request - Provider: {self.provider_name} - Model: {self.model} - ReqID: {req_id}")

        try:
            async with self.client.stream("POST", "/api/generate", json=payload) as response:
                response.raise_for_status()
                async for chunk in response.aiter_lines():
                    if chunk:
                        data = json.loads(chunk)
                        yield data.get("response", "")
        except httpx.ReadTimeout:
            raise LLMTimeoutException("Ollama streaming timed out")
        except httpx.ConnectError:
            raise ProviderUnavailableException("Ollama API is unreachable")
        except Exception as e:
            raise LLMException(f"Streaming failed: {str(e)}")

    async def health_check(self) -> Dict[str, Any]:
        start_time = time.time()
        healthy = False
        try:
            response = await self.client.get("/")
            if response.status_code == 200:
                healthy = True
        except Exception:
            pass
            
        latency = (time.time() - start_time) * 1000
        return {
            "provider": self.provider_name,
            "model": self.model,
            "healthy": healthy,
            "latency_ms": latency
        }
