# Ollama Integration Plan

## Selected Integration Point
The most optimal, lowest-risk integration point is to utilize the existing LLMFactory and OllamaProvider ecosystem.

## Action Items
1. **Preserve pp/api/routes/chat.py**: Do not modify the endpoint contract.
2. **Update Composition Root**: Modify pp/chat/bootstrap.py to call LLMFactory.get_provider() instead of manually constructing LLM classes.
3. **Configuration**: Ensure .env includes LLM_PROVIDER=ollama and OLLAMA_MODEL=qwen2.5:7b.
4. **Remove Hacks**: Remove any inline DummyLLM or OllamaLLMService hacks previously placed in the bootstrap layer.

## Justification
This strategy preserves Dependency Injection, adheres to the Thin Orchestrator paradigm, and requires exactly 0 lines of new boilerplate logic, as the foundational OllamaProvider has already been built into the enterprise architecture.
