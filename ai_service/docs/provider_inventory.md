# Provider Inventory

## LLM Abstractions
- ILLMService: Base interface for text generation and streaming.
- BaseLLMProvider: Abstract base class implementing foundational provider behaviors.

## Concrete Providers
- DummyLLM: Used for unit testing and offline development.
- BedrockProvider: AWS Bedrock integration (e.g., Claude 3).
- **OllamaProvider**: Native integration using httpx.AsyncClient targeting local models.

## Factories
- LLMFactory: Core DI provider resolver. Reads settings.LLM_PROVIDER to return the singleton instance.
