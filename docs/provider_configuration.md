# Provider Configuration

## LLM Factory
The AI Assistant relies on a dynamic LLMFactory that switches providers based on the LLM_PROVIDER environment variable.

### Supported Providers
- **ollama**: For local, offline deployment using Ollama.
- **omniroute**: For local deployment using the OmniRoute AI API.
- **bedrock**: For production deployment using AWS Bedrock.
- **auto**: Resolves to ollama in development, bedrock in production.

Switch providers by simply updating LLM_PROVIDER in your .env.
