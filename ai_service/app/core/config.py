from typing import Optional
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration managed by Pydantic.
    Required fields without defaults fail startup if not provided in the env.

    DEPLOYMENT MODE (single switch):
      DEVELOPMENT_MODE=true  -> OmniRoute/local models, local MCP, DEBUG logging.
      DEVELOPMENT_MODE=false -> DeepSeek API, production config, INFO logging.

    Environment-specific values derive from this flag unless explicitly set.
    See _apply_mode_defaults.
    """
    # Application
    APP_NAME: str = "BlueTeamers AI Service"
    APP_VERSION: str = "1.0.0"

    # Deployment mode. This is THE single switch for development vs production.
    # When true the app behaves as a local development environment (OmniRoute,
    # verbose logging, permissive defaults). When false it behaves as a production
    # deployment (DeepSeek API, restrained logging, secure defaults).
    DEVELOPMENT_MODE: bool = True

    # Derived from DEVELOPMENT_MODE; set automatically (see _apply_mode_defaults).
    APP_ENV: Optional[str] = None
    ENVIRONMENT: Optional[str] = None
    DEBUG: Optional[bool] = None

    # Demo Mode
    ENABLE_DEMO_MODE: bool = False
    DEMO_USER_EMAIL: Optional[str] = None
    DEMO_USER_PASSWORD: Optional[str] = None

    # Security
    SECRET_KEY: str
    JWT_SECRET: str
    # Shared secret for gating internal/admin operations (knowledge ingest,
    # platform debug endpoints). Leave unset in development; REQUIRED in
    # production so the /api/knowledge/* and /debug routes stay locked.
    INTERNAL_ADMIN_TOKEN: Optional[str] = None
    # Path to the RS256 public key used to verify Django-issued JWTs in the
    # AI service's protected endpoints. When set and the file exists, the
    # JWTValidator accepts only RS256. Leave empty to fall back to the legacy
    # symmetric JWT_SECRET behavior.
    JWT_PUBLIC_KEY_PATH: str = ""
    # Optional expected issuer/audience claims. When set, tokens missing or
    # mismatching these claims are rejected (defense against cross-service
    # token reuse). Leave empty to skip the check.
    JWT_ISSUER: Optional[str] = None
    JWT_AUDIENCE: Optional[str] = None
    # Resolved per mode: development -> ["*"], production -> [].
    # Production must set CORS_ORIGINS explicitly.
    CORS_ORIGINS: list[str] = []

    # Django Integration
    DJANGO_API_URL: str

    # Database (currently unused by the app; kept optional for future use)
    POSTGRES_URL: Optional[str] = None

    # Cache
    CACHE_ENABLED: bool = True
    CACHE_VERSION: str = "v1"
    CACHE_TTL: int = 3600
    CACHE_MAX_SIZE: int = 1000
    CACHE_BACKEND: str = "memory"
    STREAMING_CACHE_DELAY_MS: int = 10
    REDIS_URL: str = "redis://localhost:6379"

    # LLM provider selection. Resolved per mode when not set explicitly:
    #   development -> "omniroute", production -> "deepseek".
    # Allowed values: "omniroute" | "deepseek" | "auto".
    LLM_PROVIDER: Optional[str] = None

    # OmniRoute (development default)
    OMNIROUTE_API_KEY: Optional[str] = None
    OMNIROUTE_BASE_URL: Optional[str] = None
    # Pinned to a single deepseek model via the local OmniRoute gateway.
    # auto/* combos degrade to low-quality free providers (single garbage
    # tokens); oc/deepseek-v4-flash-free answers fully and keeps context.
    OMNIROUTE_MODEL: str = "oc/deepseek-v4-flash-free"

    # DeepSeek official API (OpenAI-compatible) — the production provider.
    # Set LLM_PROVIDER=deepseek to use it. The key lives in .env (gitignored);
    # NEVER hardcode it.
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-v4-flash"
    # Optional hard cap on output tokens per LLM call (all providers). Set in
    # .env to bound spend while testing (e.g. LLM_MAX_TOKENS=256); None = no cap.
    LLM_MAX_TOKENS: Optional[int] = None

    # MCP servers (config-driven; see app/mcp/config.py).
    #   MCP_SERVERS_CONFIG: inline JSON string, e.g.
    #     {"servers": {"filesystem": {
    #        "transport": "stdio",
    #        "command": "npx",
    #        "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]}}}
    #   MCP_SERVERS_CONFIG_PATH: path to a JSON file with the same shape.
    MCP_ENABLED: bool = True
    MCP_SERVERS_CONFIG: Optional[str] = None
    MCP_SERVERS_CONFIG_PATH: str = ""

    # Vector Database
    VECTOR_DB_PATH: str = "./vector_store"

    # Chunking
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 120
    MAX_DOCUMENT_SIZE_MB: int = 5

    # Embeddings
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DEVICE: str = "cpu"
    EMBEDDING_BATCH_SIZE: int = 32
    EMBEDDING_NORMALIZE: bool = True

    # Vector Store
    VECTOR_STORE: str = "faiss"
    VECTOR_INDEX_TYPE: str = "IndexFlatIP"
    VECTOR_PATH: str = "./vector_store/index.faiss"
    VECTOR_METADATA_FILE: str = "./vector_store/metadata.json"
    TOP_K_DEFAULT: int = 5

    # Indexing
    INDEX_BATCH_SIZE: int = 10
    MAX_CONCURRENT_DOCUMENTS: int = 5
    RETRY_COUNT: int = 3

    # Knowledge Ingestion (static course knowledge -> vector DB)
    KNOWLEDGE_LESSON_JSON: str = "./app/knowledge/data/all_lessons.json"
    KNOWLEDGE_COURSE_JSON: str = "./app/knowledge/data/course_catalog.json"
    KNOWLEDGE_INGEST_ON_STARTUP: bool = True
    KNOWLEDGE_BATCH_SIZE: int = 32

    # Retrieval
    DEFAULT_TOP_K: int = 5
    MAX_TOP_K: int = 20
    MIN_SIMILARITY_SCORE: float = 0.4

    # Context Builder
    MAX_CONTEXT_TOKENS: int = 4000

    # Prompt Builder
    MAX_PROMPT_TOKENS: int = 8000

    # Logging
    # Resolved per mode: development -> DEBUG, production -> INFO.
    LOG_LEVEL: Optional[str] = None

    # Memory
    MEMORY_ENABLED: bool = True
    MEMORY_WINDOW: int = 10
    # Filesystem path for the SQLite conversation-memory store. Relative paths
    # resolve against the AI service working directory.
    MEMORY_DB_PATH: str = "data/memory.db"

    # Chat endpoint rate limiting (in-process fixed window, per user/IP).
    CHAT_RATE_LIMIT_ENABLED: bool = True
    CHAT_RATE_LIMIT: int = 60
    CHAT_RATE_WINDOW_SECONDS: int = 60
    MAX_SESSION_MESSAGES: int = 50

    # Freemium AI access (Sprint 5)
    # Users without any paid course get a limited number of AI messages per day
    # via the floating assistant; course purchasers get unlimited access.
    FREEMIUM_ENABLED: bool = True
    # How many user-triggered AI requests a free user may make per reset interval.
    FREEMIUM_FREE_MESSAGE_LIMIT: int = 5
    # Reset policy: "daily" resets the counter every UTC day; "never" disables
    # the reset (the counter only grows until the user upgrades). Configurable.
    FREEMIUM_RESET_POLICY: str = "daily"
    # Purchase statuses (comma-separated) that grant premium access. The Django
    # payments app marks a purchase as "paid" once Razorpay confirms payment.
    FREEMIUM_PREMIUM_PURCHASE_STATUSES: str = "paid"
    # Feature flag for the /chat full-workspace premium gate.
    FREEMIUM_PREMIUM_CHAT_GATE: bool = True
    # Filesystem path for the SQLite freemium usage store.
    FREEMIUM_DB_PATH: str = "data/freemium.db"

    # Cost Optimization Layer (Sprint 6)
    # Recent Conversations & Favorites
    # Filesystem path for the SQLite conversation store (metadata + messages).
    CONVERSATIONS_DB_PATH: str = "data/conversations.db"
    # How many conversation summaries to return per page (lazy loading).
    CONVERSATIONS_PAGE_SIZE: int = 20
    # Maximum conversation title length auto-generated / accepted.
    CONVERSATION_TITLE_MAX_LEN: int = 60
    # Persist chat turns to the conversation store when enabled.
    CONVERSATION_PERSISTENCE_ENABLED: bool = True

    # Assessment Agent (interactive learning & quiz agent)
    ENABLE_ASSESSMENT_AGENT: bool = True
    ASSESSMENT_MINIMUM_CONFIDENCE_THRESHOLD: float = 0.6
    ASSESSMENT_DEFAULT_QUIZ_LENGTH: int = 5
    ASSESSMENT_DEFAULT_DIFFICULTY: str = "beginner"
    ASSESSMENT_MAXIMUM_QUESTIONS: int = 10
    ASSESSMENT_ALLOW_ADAPTIVE_DIFFICULTY: bool = True

    # Course-aware Assessment Agent
    # Only ever offer a quiz when the user is enrolled in a course whose topic the
    # question belongs to; otherwise defer to the Course Recommendation service.
    ASSESSMENT_REQUIRE_ENROLLMENT: bool = True
    # Number of seconds after a completed assessment during which we do NOT offer
    # another quiz for the same course (defaults to 7 days).
    ASSESSMENT_RECENT_WINDOW_SECONDS: int = 604800
    # How many recommended courses to surface when the user is not enrolled.
    ASSESSMENT_COURSE_RECOMMENDATION_COUNT: int = 3

    # Observability
    OBSERVABILITY_ENABLED: bool = True
    METRICS_PROVIDER: str = "prometheus"
    TRACING_PROVIDER: str = "native"
    METRICS_ENDPOINT: str = "/metrics"
    TRACING_ENABLED: bool = True
    LOGGING_ENABLED: bool = True
    METRICS_ENABLED: bool = True

    SERVICE_NAME: str = "Enterprise AI Service"
    SERVICE_VERSION: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    @model_validator(mode="after")
    def _apply_mode_defaults(self) -> "Settings":
        """
        Single source of truth for deployment-mode defaults.

        DEVELOPMENT_MODE=true  -> OmniRoute + local models, permissive CORS, DEBUG.
        DEVELOPMENT_MODE=false -> DeepSeek API, INFO logging, secure defaults.

        Any field already provided explicitly via the environment is respected;
        only unset fields are filled with the mode-appropriate value.
        """
        dev = bool(self.DEVELOPMENT_MODE)

        # Always keep derived markers consistent with the mode switch.
        self.APP_ENV = "development" if dev else "production"
        self.ENVIRONMENT = self.APP_ENV
        self.DEBUG = dev

        if not self.LLM_PROVIDER:
            self.LLM_PROVIDER = "omniroute" if dev else "deepseek"

        if not self.OMNIROUTE_BASE_URL:
            self.OMNIROUTE_BASE_URL = "http://localhost:20128/v1"

        if not self.LOG_LEVEL:
            self.LOG_LEVEL = "DEBUG" if dev else "INFO"

        if not self.CORS_ORIGINS:
            self.CORS_ORIGINS = ["*"] if dev else []

        # Production must not run with a wildcard/empty CORS list: wildcard with
        # credentials is rejected by browsers and empty silently breaks the API.
        # Fail fast so the operator sets explicit origins.
        if not dev:
            if not self.CORS_ORIGINS or self.CORS_ORIGINS == ["*"]:
                raise ValueError(
                    "Production requires explicit CORS_ORIGINS (e.g. "
                    '"https://www.infosecdairies.io,https://infosecdairies.io"). '
                    "Wildcard or empty is not allowed with credentials."
                )

        return self

    @property
    def is_development(self) -> bool:
        """True in development mode, False in production mode."""
        return bool(self.DEVELOPMENT_MODE)

    @property
    def is_production(self) -> bool:
        """True in production mode (DeepSeek API deployment)."""
        return not self.is_development


# Singleton instance to be imported across the application
settings = Settings()
