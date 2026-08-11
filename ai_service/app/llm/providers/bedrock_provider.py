import time
import asyncio
import logging
import threading
import queue
from typing import AsyncGenerator, Dict, Any, List, Optional

from app.core.config import settings
from app.core.logging import request_id_var
from app.llm.base import BaseLLMProvider
from app.llm.schemas import LLMRequest, LLMResponse
from app.llm.exceptions import (
    ProviderConfigurationException,
    ProviderUnavailableException,
    LLMException,
)

logger = logging.getLogger("app.llm.bedrock")

_DEFAULT_MAX_TOKENS = 4096


class BedrockProvider(BaseLLMProvider):
    """
    AWS Bedrock implementation for scalable production deployment.

    Uses the Bedrock Runtime Converse API (boto3) so text, images and
    streaming all work through a single code path. Claude 3 family models
    (e.g. anthropic.claude-3-sonnet-20240229-v1:0) are vision-capable, so
    image attachments are forwarded as multimodal content blocks.
    """

    def __init__(self):
        self.region = settings.BEDROCK_REGION
        self.model = settings.BEDROCK_MODEL
        self.provider_name = "bedrock"

        if not self.region or not self.model:
            raise ProviderConfigurationException(
                "Bedrock region and model must be configured."
            )

        self._client = None
        self._client_error: Optional[str] = None

    # ------------------------------------------------------------------ #
    # Client bootstrap
    # ------------------------------------------------------------------ #
    def _get_client(self):
        """Lazily create (and cache) the bedrock-runtime boto3 client."""
        if self._client is not None:
            return self._client
        try:
            import boto3

            client = boto3.client("bedrock-runtime", region_name=self.region)
            self._client = client
            self._client_error = None
            return client
        except Exception as e:
            self._client_error = str(e)
            raise ProviderConfigurationException(
                f"Unable to initialize AWS Bedrock client: {e}"
            )

    @staticmethod
    def _build_content(request: LLMRequest) -> List[Dict[str, Any]]:
        """Build the user message content blocks (text + optional images)."""
        content: List[Dict[str, Any]] = []
        if request.prompt:
            content.append({"text": request.prompt})
        for img in (request.images or []):
            raw = img.get("bytes")
            if not raw:
                continue
            fmt = img.get("format") or "png"
            content.append({
                "image": {
                    "format": fmt,
                    "source": {"bytes": raw},
                }
            })
        return content

    def _converse_kwargs(self, request: LLMRequest) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {
            "modelId": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": self._build_content(request),
                }
            ],
            "inferenceConfig": {
                "temperature": request.temperature,
                "maxTokens": request.max_tokens or _DEFAULT_MAX_TOKENS,
            },
        }
        if request.system_prompt:
            kwargs["system"] = [{"text": request.system_prompt}]
        return kwargs

    # ------------------------------------------------------------------ #
    # Non-streaming
    # ------------------------------------------------------------------ #
    async def generate(self, request: LLMRequest) -> LLMResponse:
        start_time = time.time()
        req_id = request_id_var.get()

        logger.info(
            f"LLM Request - Provider: {self.provider_name} - Model: {self.model} "
            f"- ReqID: {req_id}"
        )

        client = self._get_client()
        kwargs = self._converse_kwargs(request)

        try:
            response = await asyncio.to_thread(
                client.converse, **kwargs
            )
        except Exception as e:
            raise self._map_error(e)

        latency = (time.time() - start_time) * 1000

        text = ""
        stop_reason = None
        usage: Dict[str, Any] = {}
        try:
            output = response.get("output", {})
            message = output.get("message", {})
            for block in message.get("content", []):
                if "text" in block:
                    text += block["text"]
            stop_reason = response.get("stopReason")
            usage = response.get("usage", {})
        except Exception:
            pass

        logger.info(
            f"LLM Response - Provider: {self.provider_name} - Model: {self.model} "
            f"- Latency: {latency:.2f} ms - ReqID: {req_id}"
        )

        return LLMResponse(
            text=text,
            provider=self.provider_name,
            model=self.model,
            latency_ms=latency,
            finish_reason=stop_reason,
            usage=usage,
        )

    # ------------------------------------------------------------------ #
    # Streaming
    # ------------------------------------------------------------------ #
    async def stream_generate(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        req_id = request_id_var.get()
        client = self._get_client()
        kwargs = self._converse_kwargs(request)

        q: "queue.Queue[Any]" = queue.Queue()
        stop = threading.Event()

        def _run():
            try:
                stream = client.converse_stream(**kwargs)
                for event in stream.get("stream", []):
                    if stop.is_set():
                        break
                    if "contentBlockDelta" in event:
                        delta = event["contentBlockDelta"].get("delta", {})
                        if "text" in delta:
                            q.put(("token", delta["text"]))
                q.put(("done", None))
            except Exception as e:
                q.put(("error", e))
            finally:
                q.put(("done", None))

        worker = threading.Thread(target=_run, daemon=True)
        worker.start()

        logger.info(
            f"LLM Stream Request - Provider: {self.provider_name} "
            f"- Model: {self.model} - ReqID: {req_id}"
        )

        try:
            while True:
                kind, payload = await asyncio.to_thread(q.get)
                if kind == "token":
                    yield payload
                elif kind == "error":
                    raise self._map_error(payload)
                else:
                    break
        finally:
            stop.set()

    # ------------------------------------------------------------------ #
    # Health
    # ------------------------------------------------------------------ #
    async def health_check(self) -> Dict[str, Any]:
        start_time = time.time()
        healthy = False
        detail = "unknown"
        try:
            self._get_client()
            import boto3

            # list_foundation_models is free and validates credentials/region.
            bedrock = boto3.client("bedrock", region_name=self.region)
            found = False
            try:
                resp = bedrock.list_foundation_models()
                found = any(
                    m.get("modelId") == self.model
                    for m in resp.get("modelSummaries", [])
                )
                healthy = True
                detail = "found" if found else "reachable"
            except Exception as e:
                detail = f"unreachable: {e}"
        except Exception as e:
            detail = str(e)

        latency = (time.time() - start_time) * 1000
        return {
            "provider": self.provider_name,
            "model": self.model,
            "healthy": healthy,
            "status": "healthy" if healthy else "unhealthy",
            "detail": detail,
            "latency_ms": latency,
        }

    def _map_error(self, e: Exception) -> Exception:
        if isinstance(e, ProviderConfigurationException):
            return e
        msg = str(e)
        if "NoCredentialsError" in msg or "Unable to locate credentials" in msg:
            return ProviderConfigurationException(
                "AWS credentials not found. Configure AWS_ACCESS_KEY_ID and "
                "AWS_SECRET_ACCESS_KEY (or an IAM role) for Bedrock access."
            )
        if "ResourceNotFound" in msg or "model not found" in msg.lower():
            return LLMException(
                f"Bedrock model '{self.model}' not found or not accessible in "
                f"region '{self.region}'."
            )
        logger.error("Bedrock call failed: %s", msg)
        return ProviderUnavailableException(f"AWS Bedrock error: {msg}")
