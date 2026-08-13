import logging
from app.core.config import settings
from app.llm.base import BaseLLMProvider
from app.llm.exceptions import ProviderConfigurationException
from app.llm.providers.ollama_provider import OllamaProvider
from app.llm.providers.bedrock_provider import BedrockProvider

logger = logging.getLogger("app.llm.factory")


class LLMFactory:
    """
    Factory for instantiating the correct LLM provider based on configuration.
    Implements a singleton pattern to reuse the provider connection pool.

    Provider selection is fully configuration-driven:
      - LLM_PROVIDER=omniroute -> OmniRoute (development default)
      - LLM_PROVIDER=deepseek  -> DeepSeek official API (real API key)
      - LLM_PROVIDER=bedrock   -> Amazon Bedrock (production default)
      - LLM_PROVIDER=ollama    -> local Ollama
      - LLM_PROVIDER=auto      -> resolved from the deployment mode
    """
    _instance: BaseLLMProvider = None

    @classmethod
    def get_provider(cls) -> BaseLLMProvider:
        if cls._instance is not None:
            return cls._instance

        provider_mode = (settings.LLM_PROVIDER or "auto").lower()
        app_mode = settings.APP_ENV.lower()
        mode = "development" if settings.is_development else "production"

        logger.info(
            f"Selecting LLM provider. Configuration: LLM_PROVIDER={provider_mode}, "
            f"APP_ENV={app_mode}, deployment_mode={mode}"
        )

        if provider_mode == "ollama":
            cls._instance = OllamaProvider()
        elif provider_mode == "bedrock":
            cls._instance = BedrockProvider()
        elif provider_mode == "deepseek":
            from app.llm.providers.deepseek_provider import DeepSeekProvider
            cls._instance = DeepSeekProvider()
        elif provider_mode == "omniroute":
            from app.llm.providers.omniroute_provider import OmniRouteProvider
            cls._instance = OmniRouteProvider()
        elif provider_mode == "auto":
            # Development uses OmniRoute/local models; production uses Amazon Bedrock.
            if settings.is_development:
                from app.llm.providers.omniroute_provider import OmniRouteProvider
                cls._instance = OmniRouteProvider()
            else:
                cls._instance = BedrockProvider()
        else:
            raise ProviderConfigurationException(
                f"Unsupported LLM_PROVIDER: {provider_mode}"
            )

        logger.info(
            "LLM provider selected: %s (mode=%s, provider=%s, model=%s)",
            cls._instance.__class__.__name__,
            mode,
            getattr(cls._instance, "provider_name", "unknown"),
            getattr(cls._instance, "model", "default"),
        )
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Drop the cached provider instance (used mainly by tests)."""
        cls._instance = None
