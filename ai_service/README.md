# BlueTeamers AI Service

The **BlueTeamers AI Service** is an Enterprise FastAPI microservice providing highly scalable Retrieval-Augmented Generation (RAG) capabilities for the BlueTeamers AI Assistant ecosystem. Designed with strict adherence to Clean Architecture and SOLID principles, this service bridges advanced language models with proprietary institutional data securely and efficiently.

This microservice supports:
- High-Performance FastAPI Asynchronous Routing
- Enterprise-grade RAG Pipelines
- FAISS Vector Store Integration
- Sentence Transformers Embedding Service
- Automated Document Chunking Pipelines
- Context & Prompt Builder Utilities
- Provider-agnostic LLM Abstraction (Ollama, AWS Bedrock)
- Deep Health Monitoring & Telemetry
- JWT Authentication Integration
- Structured Request Logging
- Advanced Dependency Injection

---

## Architecture

The BlueTeamers AI Assistant utilizes a clean, decoupled architecture. The frontend application interfaces exclusively with the Django REST API, which forwards securely authenticated AI queries down to this FastAPI AI Service.

```text
React Frontend
      │
      ▼
Django REST API (Gateway & Auth)
      │
      ▼
FastAPI AI Service
      │
      ├── Chat API            # Handles HTTP lifecycle, validation, and JSON mapping
      ├── Health API          # Aggregates async health probes across dependencies
      ├── RAG Engine          # Orchestrates the RAG lifecycle pipeline purely in memory
      ├── Retriever           # Connects to Vector Stores (FAISS) to fetch metadata & indices
      ├── Context Builder     # Formats and enforces token budgets on retrieved docs
      ├── Prompt Builder      # Merges context with robust LLM system instructions
      ├── LLM Provider        # Standardized abstraction for Ollama / AWS Bedrock
      └── Vector Store        # FAISS implementation mapped with a JSON Metadata Store
```

### Layer Responsibilities
- **Application Layer (`app/main.py`)**: Responsible ONLY for composition, routing, and lifecycle events. Contains zero business logic.
- **Service Layer (`app/chat`, `app/rag`)**: Responsible for API schema mappings and pipeline orchestration.
- **Domain/Infrastructure Layer (`app/llm`, `app/vector_store`, `app/embeddings`)**: Responsible for executing I/O bound tasks using strict interface abstractions.

---

## Project Structure

```text
ai_service/app/
├── chat/               # Chat API routing, schemas, and dependencies
├── chunking/           # Text splitting and overlap logic
├── context/            # Budget-aware prompt context construction
├── core/               # App configuration, structured logging, middleware
├── embeddings/         # Sentence Transformers local embedding generation
├── indexing/           # Document ingestion and vectorization pipelines
├── llm/                # Abstract LLM Provider implementations
├── prompt_builder/     # Advanced system prompting and templating
├── rag/                # RAG Orchestration Engine
├── retrieval/          # Semantic search wrappers and reranking stubs
├── vector_store/       # FAISS indexing and JSON metadata storage
├── exception_handlers.py # Global fault interception
├── health.py             # Asynchronous health aggregation endpoint
├── lifecycle.py          # FastAPI lifespan hooks
├── main.py               # Uvicorn entry point
└── middleware.py         # CORS and Logging request interception
```

---

## Features

- ✔ **Configuration Management** (Pydantic Settings)
- ✔ **Structured Logging** (Sub-millisecond tracking & Request UUIDs)
- ✔ **JWT Authentication** (Stateless payload validation)
- ✔ **API Discovery** (OpenAPI / Swagger)
- ✔ **Embedding Service** (Local BAAI/bge-small-en-v1.5)
- ✔ **Chunking** (Overlap and Max-Size enforcement)
- ✔ **FAISS Vector Store** (Local FlatIP indexing + Metadata linkage)
- ✔ **Indexing Pipeline** (Document ingestion)
- ✔ **Retrieval** (Semantic thresholding)
- ✔ **Context Builder** (Token-budgeting logic)
- ✔ **Prompt Builder** (System instruction assembly)
- ✔ **RAG Engine** (Centralized orchestration)
- ✔ **Chat API** (HTTP routing and validation)
- ✔ **Health Monitoring** (Parallel dependency probing)
- ✔ **Middleware** (Config-driven CORS)
- ✔ **Exception Handling** (Stack-trace shielding)
- ✔ **Dependency Injection** (FastAPI `Depends`)
- ✔ **Unit Tests** (Comprehensive Pytest coverage)

---

## Technology Stack

| Component | Technology | Use Case |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core Application |
| **Framework** | FastAPI | High-performance Async API |
| **Validation** | Pydantic V2 | Settings & Schema validation |
| **Vector DB** | FAISS | In-memory similarity search |
| **Embeddings** | Sentence Transformers | Local semantic vectorization |
| **LLM (Local)** | Ollama | Local development inference |
| **LLM (Cloud)** | AWS Bedrock | *Planned optional cloud fallback* |
| **Testing** | Pytest | Unit & Integration testing |

---

## Installation

### 1. Clone the repository
```bash
git clone <repository_url>
cd BlueTeamers-AI-Assistant/ai_service
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Unix or MacOS:
source .venv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Update `.env` with your secure configuration parameters.

---

## Environment Variables

| Name | Purpose | Required | Default |
| :--- | :--- | :--- | :--- |
| `APP_NAME` | OpenAPI Title | No | BlueTeamers AI Service |
| `APP_VERSION` | API Version | No | 1.0.0 |
| `APP_ENV` | Application Environment | No | development |
| `SECRET_KEY` | Cryptographic application secret | **Yes** | - |
| `JWT_SECRET` | Secret to decode Django JWTs | **Yes** | - |
| `CORS_ORIGINS` | Allowed cross-origin lists (JSON list) | No | `["*"]` |
| `DJANGO_API_URL` | Upstream Django API endpoint | **Yes** | - |
| `POSTGRES_URL` | Database connection string | **Yes** | - |
| `REDIS_URL` | Cache connection string | **Yes** | - |
| `LLM_PROVIDER` | `ollama` or `bedrock` | No | auto |
| `OLLAMA_BASE_URL` | Local LLM host | No | http://localhost:11434 |
| `OLLAMA_MODEL` | Local LLM Model identifier | No | llama3 |
| `BEDROCK_REGION` | AWS Bedrock deployment region | No | us-east-1 |
| `BEDROCK_MODEL` | AWS Bedrock model identifier | No | anthropic.claude-3... |
| `VECTOR_DB_PATH`| FAISS index location | No | ./vector_store |
| `CHUNK_SIZE` | Max text chunk size | No | 600 |
| `CHUNK_OVERLAP` | Overlap window between chunks | No | 120 |
| `EMBEDDING_MODEL` | Local transformer model | No | BAAI/bge-small-en-v1.5 |

---

## Running the Application

**Run in Development Mode (Live Reload):**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Run in Production:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Running Tests

The test suite covers the entire RAG pipeline and API endpoints.

**Run All Tests:**
```bash
pytest
```

**Run a Single File:**
```bash
pytest tests/test_rag.py
```

---

## API Documentation

When the server is running, interactive API documentation is automatically generated.

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Core Endpoints

- `GET /`: Lightweight uptime pulse indicating service presence.
- `GET /health`: Deep, parallel asynchronous evaluation of all downstream integrations (Vector Store, LLM Provider, Embedding Models).
- `POST /api/v1/chat`: Primary completion endpoint. Accepts `query` and orchestrates the complete RAG Engine lifecycle.
- `GET /api/v1/chat/health`: Sub-router health aggregator.

---

## Configuration

The service leverages a highly decoupled, state-isolated configuration via Pydantic Settings:
- **CORS**: Securely managed via `CORS_ORIGINS`. Defaults to `["*"]` for development.
- **Logging**: Globally managed in `app/core/logging.py`, leveraging sub-millisecond JSON metrics and Request UUIDs payload injection, guaranteeing no PII or secure tokens are logged natively.
- **JWT**: Authenticates strictly against the underlying Django REST API architecture's secrets.
- **LLM Provider**: Interface abstraction manages seamless hot-swapping between `OllamaProvider` (local offline AI) and `AWSBedrockProvider` using `LLM_PROVIDER`.
- **Vector Store**: Natively couples unstructured `FAISS` indexing alongside structural JSON `metadata.json` stores for rich data traversal.

---

## Design Principles

This project was built from the ground up prioritizing enterprise stability:
- **Clean Architecture**: Hard boundaries exist between the API routers, the RAG orchestration, and the I/O providers (FAISS, Ollama).
- **SOLID Principles**: Components utilize strict interfaces (`BaseRetriever`, `BaseLLMProvider`), allowing hot-swapping integrations without refactoring business logic.
- **Dependency Injection**: FastAPI `Depends()` is utilized universally. No services instantiate their own dependencies internally, ensuring native testability.
- **Stateless Services**: All state is localized to the Request Context, making the application 100% horizontally scalable.
- **Separation of Concerns**: Middlewares handle telemetry, Exception Handlers trap stack traces, and routers simply pipe requests.

---

## Current Status

**Version 1.0 (Completed)**

The following base modules have achieved production readiness:
- Configuration
- Logging
- Authentication
- API Discovery
- Chunking
- Embeddings
- Vector Store
- Indexing
- Retrieval
- Context Builder
- Prompt Builder
- RAG Engine
- Chat API
- FastAPI Integration
- Health Monitoring

---

## Future Roadmap

Planned enhancements to the ecosystem:
- Django Integration
- React Integration
- Streaming Responses
- Conversation Memory
- LangGraph
- Tool Calling
- Guardrails
- Rate Limiting
- Observability

---

## Contributing

1. Ensure changes align with the existing **Clean Architecture** patterns.
2. Verify all `pydantic` schemas are rigorously typed.
3. Keep all side-effects and network calls masked behind an abstract base class (`ABC`).
4. **All** Pull Requests must pass the existing `pytest` test suite without degradation.
5. Do not circumvent the `app.core.logging` structures.

---

## License

MIT License (Placeholder)
