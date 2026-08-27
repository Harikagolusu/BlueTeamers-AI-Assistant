import time
import json
import logging
import httpx
from typing import AsyncGenerator, Dict, Any

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

logger = logging.getLogger("app.llm.deepseek")

# deepseek-v4-flash official pricing (per 1K tokens), as of 2026:
#   input (cache miss) $0.14/M, cache-hit input $0.0028/M, output $0.28/M.
# Used only to log an approximate spend per call so testers can watch balance.
_DEEPSEEK_INPUT_RATE_PER_1K = 0.00014
_DEEPSEEK_CACHE_HIT_RATE_PER_1K = 0.0000028
_DEEPSEEK_OUTPUT_RATE_PER_1K = 0.00028


class DeepSeekProvider(BaseLLMProvider):
    """Official DeepSeek API via the OpenAI-compatible chat completions endpoint.

    Returns a proper JSON body for ``stream=False`` and an SSE stream for
    ``stream=True``, which the streaming path in the chat pipeline consumes.
    """

    def __init__(self):
        if not settings.DEEPSEEK_API_KEY:
            raise ProviderConfigurationException(
                "DEEPSEEK_API_KEY is required when using the DeepSeek provider"
            )

        self.base_url = (settings.DEEPSEEK_BASE_URL or "").rstrip('/')
        self.model = settings.DEEPSEEK_MODEL

        limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
        timeout = httpx.Timeout(120.0, connect=5.0)
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=headers, limits=limits, timeout=timeout)
        self.provider_name = "deepseek"

    async def close(self):
        await self.client.aclose()

    def _build_messages(self, request: LLMRequest) -> list:
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        return messages

    def _max_tokens(self, request: LLMRequest) -> Dict[str, Any]:
        """Return the payload fragment capping output tokens, if configured.

        The global ``settings.LLM_MAX_TOKENS`` is the safety net; an explicit
        per-request ``max_tokens`` wins when both are set.
        """
        cap = request.max_tokens or settings.LLM_MAX_TOKENS
        return {"max_tokens": cap} if cap else {}

    def _log_usage(self, request: LLMRequest, data: Dict[str, Any], latency: float, req_id: str) -> None:
        """Log token usage + approximate spend so testers can track their balance."""
        usage = data.get("usage") or {}
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
        # DeepSeek auto-caches the prompt prefix; cached input bills much lower.
        cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens", 0)
        uncached = max(0, prompt_tokens - cached)
        cost = (
            uncached / 1000 * _DEEPSEEK_INPUT_RATE_PER_1K
            + cached / 1000 * _DEEPSEEK_CACHE_HIT_RATE_PER_1K
            + completion_tokens / 1000 * _DEEPSEEK_OUTPUT_RATE_PER_1K
        )
        logger.info(
            "DeepSeek usage - ReqID: %s - model: %s - prompt_tokens: %d "
            "(cached %d), completion_tokens: %d, total: %d, est_cost: $%.5f - latency: %.2f ms",
            req_id, self.model, prompt_tokens, cached, completion_tokens,
            total_tokens, cost, latency,
        )

        # Record the real token usage into the per-user accounting ledger so the
        # runtime token quota actually sees it (and colleagues testing the bot
        # produce measurable usage). Runs for both the streaming and the
        # non-streaming path because this method is their shared choke point.
        try:
            from app.runtime.models.context import TokenUsage
            from app.runtime.services.accounting_service import TokenAccountant
            TokenAccountant().add_usage(
                TokenUsage(
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    cached_tokens=cached,
                    tool_tokens=0,
                )
            )
        except Exception:
            # Accounting must never break generation; failures are just logged.
            logger.warning("Failed to record token usage into runtime ledger", exc_info=True)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        start_time = time.time()
        req_id = request_id_var.get()

        payload = {
            "model": self.model,
            "messages": self._build_messages(request),
            "stream": False,
            "temperature": request.temperature,
            # V4 Flash defaults to thinking mode; disable it for a fast, cheap
            # chat assistant (no reasoning-token overhead).
            "thinking": {"type": "disabled"},
            **self._max_tokens(request),
        }

        try:
            logger.info(f"LLM Request - Provider: {self.provider_name} - Model: {self.model} - ReqID: {req_id}")
            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()

            data = response.json()
            latency = (time.time() - start_time) * 1000

            self._log_usage(request, data, latency, req_id)

            text = ""
            choices = data.get("choices", [])
            if choices and len(choices) > 0:
                text = choices[0].get("message", {}).get("content", "")

            usage = data.get("usage", {})
            finish_reason = choices[0].get("finish_reason", "stop") if choices else "stop"
            if finish_reason == "length" and text:
                text += self.TRUNCATION_NOTICE

            return LLMResponse(
                text=text,
                provider=self.provider_name,
                model=self.model,
                latency_ms=latency,
                finish_reason=finish_reason,
                usage={
                    "prompt_eval_count": usage.get("prompt_tokens", 0),
                    "eval_count": usage.get("completion_tokens", 0),
                    "total_tokens": usage.get("total_tokens", 0),
                },
            )

        except httpx.ReadTimeout:
            logger.error(f"LLM Timeout - Provider: {self.provider_name} - ReqID: {req_id}")
            raise LLMTimeoutException("DeepSeek generation timed out")
        except httpx.ConnectError:
            logger.error(f"LLM Connection Error - Provider: {self.provider_name} - ReqID: {req_id}")
            raise ProviderUnavailableException("DeepSeek API is unreachable")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.error(f"LLM Model Not Found - Model: {self.model} - ReqID: {req_id}")
                raise ModelNotFoundException(f"DeepSeek model '{self.model}' not found")
            elif e.response.status_code == 401:
                logger.error(f"LLM Unauthorized Error - Invalid API Key - ReqID: {req_id}")
                raise LLMException("DeepSeek authentication failed. Invalid API Key.")
            logger.error(f"LLM HTTP Error - Status: {e.response.status_code} - ReqID: {req_id}")
            raise LLMException(f"DeepSeek returned error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"LLM Unexpected Error - ReqID: {req_id} - Error: {str(e)}")
            raise LLMException(f"Unexpected error in DeepSeek provider: {str(e)}")

    # Emitted when a streamed reply is hard-truncated by the max_tokens cap, so
    # the UI shows a clear notice instead of silently stopping mid-sentence.
    TRUNCATION_NOTICE = (
        "\n\n_[⚠️ This reply hit the token limit and was cut off. "
        "Reply \"continue\" to get the rest.]_"
    )

    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        req_id = request_id_var.get()
        payload = {
            "model": self.model,
            "messages": self._build_messages(request),
            "stream": True,
            "temperature": request.temperature,
            "thinking": {"type": "disabled"},
            **self._max_tokens(request),
        }

        logger.info(f"LLM Stream Request - Provider: {self.provider_name} - Model: {self.model} - ReqID: {req_id}")

        try:
            finish_reason = None
            async with self.client.stream("POST", "/chat/completions", json=payload) as response:
                response.raise_for_status()
                async for chunk in response.aiter_lines():
                    if chunk.startswith("data: "):
                        data_str = chunk[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            usage = data.get("usage")
                            if usage:
                                # DeepSeek emits the final token+usage in the
                                # last data chunk; report spend once.
                                self._log_usage(
                                    request, {"usage": usage}, 0.0, req_id
                                )
                            choices = data.get("choices", [])
                            if choices and len(choices) > 0:
                                # The final chunk carries finish_reason
                                # ("stop" | "length") so we can detect replies
                                # truncated by the max_tokens cap.
                                fr = choices[0].get("finish_reason")
                                if fr:
                                    finish_reason = fr
                                delta = choices[0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
            if finish_reason == "length":
                yield self.TRUNCATION_NOTICE
        except httpx.ReadTimeout:
            raise LLMTimeoutException("DeepSeek streaming timed out")
        except httpx.ConnectError:
            raise ProviderUnavailableException("DeepSeek API is unreachable")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise LLMException("DeepSeek authentication failed. Invalid API Key.")
            raise LLMException(f"DeepSeek returned error: {e.response.status_code}")
        except Exception as e:
            raise LLMException(f"Streaming failed: {str(e)}")

    async def health_check(self) -> Dict[str, Any]:
        start_time = time.time()
        healthy = False
        try:
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
            "latency_ms": latency,
        }
