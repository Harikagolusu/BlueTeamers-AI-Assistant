# Ollama Integration Architecture Audit

## 1. Chat Entry Point
- **Route:** pp/api/routes/chat.py (@router.post(/))
- **Service:** ChatService orchestrates execution via ChatOrchestrator.
- **Dependencies:** Injected via get_chat_service() from pp/chat/bootstrap.py.

## 2. Chat Bootstrap / Composition Root
- **File:** pp/chat/bootstrap.py
- **LLM Instantiation:** The OllamaLLMService (or LLMFactory.get_provider()) is instantiated here.
- **RAG & Memory:** RedisMemoryManager and FAISSRetriever are passed into the pipeline stages.
- **Tool Registry:** Bound via ToolProviderResolver and LegacyToolProvider.

## 3. LLM Layer
- **Interface:** ILLMService and BaseLLMProvider.
- **Factory:** LLMFactory (pp/llm/factory.py) dynamically selects between Ollama, Bedrock, and Dummy based on LLM_PROVIDER.
- **Providers:** OllamaProvider already exists natively in pp/llm/providers/ollama_provider.py.

## 4. RAG Pipeline
- **Flow:** User Query -> IntentAnalysisStage -> RagExecutionEngine -> FAISSRetriever -> PromptBuilder -> LLMService.generate/stream.

## 5. Tool Calling
- **Flow:** Orchestrator (Intent/Routing) sets target tool -> ToolExecutionEngine resolves provider -> local execution without native LLM tool binding.

## 6. Agent Orchestration
- **Flow:** Platform orchestrator routes to AGENT engine (AgentExecutor), which maintains its own capability registry and scheduler.

## 7. Streaming Pipeline
- **Flow:** ILLMService.stream_generate() yields async tokens -> Engine wraps generator in ExecutionResult -> chat_endpoint returns StreamingResponse.

## 8. Configuration
- **Mechanism:** pydantic_settings inside pp/core/config.py. 
- **Ollama Specifics:** Driven by LLM_PROVIDER=ollama and OLLAMA_MODEL=qwen2.5:7b.
