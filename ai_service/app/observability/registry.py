from prometheus_client import Counter, Gauge, Histogram, REGISTRY

class MetricsRegistry:
    """
    Central registry for all Prometheus metrics.
    Ensures metrics are instantiated exactly once to avoid DuplicateRegistration errors.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsRegistry, cls).__new__(cls)
            cls._instance._initialize_metrics()
        return cls._instance

    def _initialize_metrics(self):
        # API Metrics
        self.api_requests_total = Counter(
            "api_requests_total",
            "Total number of API requests",
            ["method", "endpoint", "status"]
        )
        self.api_requests_active = Gauge(
            "api_requests_active",
            "Number of active API requests",
            ["method", "endpoint"]
        )
        self.api_request_duration_seconds = Histogram(
            "api_request_duration_seconds",
            "Duration of API requests in seconds",
            ["method", "endpoint", "status"]
        )

        # AI Metrics
        self.ai_llm_requests_total = Counter(
            "ai_llm_requests_total",
            "Total LLM requests",
            ["provider", "model", "status"]
        )
        self.ai_retrieval_duration_seconds = Histogram(
            "ai_retrieval_duration_seconds",
            "Duration of vector retrieval in seconds",
            ["vector_store"]
        )
        self.ai_embedding_generation_seconds = Histogram(
            "ai_embedding_generation_seconds",
            "Duration of embedding generation in seconds",
            ["model"]
        )
        self.ai_prompt_generation_seconds = Histogram(
            "ai_prompt_generation_seconds",
            "Duration of prompt building in seconds"
        )
        self.ai_context_building_seconds = Histogram(
            "ai_context_building_seconds",
            "Duration of context building in seconds"
        )
        self.ai_prompt_size_bytes = Histogram(
            "ai_prompt_size_bytes",
            "Size of the generated prompt payload in bytes"
        )
        self.ai_retrieved_documents_count = Histogram(
            "ai_retrieved_documents_count",
            "Number of documents retrieved from vector store",
            ["vector_store"]
        )
        self.ai_context_size_bytes = Histogram(
            "ai_context_size_bytes",
            "Size of the built context document in bytes"
        )
        self.ai_llm_token_usage_total = Counter(
            "ai_llm_token_usage_total",
            "Total LLM tokens used",
            ["provider", "model", "type"] # type can be 'prompt' or 'completion'
        )
        self.ai_llm_provider_response_seconds = Histogram(
            "ai_llm_provider_response_seconds",
            "Time to first token / provider response latency",
            ["provider", "model"]
        )

        # Cache Metrics
        self.cache_hits_total = Counter(
            "cache_hits_total",
            "Total cache hits",
            ["cache_backend"]
        )
        self.cache_misses_total = Counter(
            "cache_misses_total",
            "Total cache misses",
            ["cache_backend"]
        )
        self.cache_lookup_latency_seconds = Histogram(
            "cache_lookup_latency_seconds",
            "Latency of cache lookup operations",
            ["cache_backend"]
        )

        # Memory Metrics
        self.conversation_memory_reads_total = Counter(
            "conversation_memory_reads_total",
            "Total reads from conversation memory"
        )
        self.conversation_memory_writes_total = Counter(
            "conversation_memory_writes_total",
            "Total writes to conversation memory"
        )
        self.conversation_active_total = Gauge(
            "conversation_active_total",
            "Total active conversations in memory",
            ["memory_backend"]
        )
        self.memory_lookup_latency_seconds = Histogram(
            "memory_lookup_latency_seconds",
            "Latency of memory lookup operations",
            ["memory_backend"]
        )

        # Streaming Metrics
        self.streaming_connections_active = Gauge(
            "streaming_connections_active",
            "Total active streaming connections",
            ["endpoint"]
        )
        self.streaming_duration_seconds = Histogram(
            "streaming_duration_seconds",
            "Duration of SSE streaming sessions"
        )
        self.streaming_errors_total = Counter(
            "streaming_errors_total",
            "Total streaming errors"
        )
        self.streaming_throughput_bytes = Counter(
            "streaming_throughput_bytes",
            "Total bytes streamed back to client"
        )

    def get_registered_count(self) -> int:
        """Return the number of metrics registered in the default registry."""
        return len(list(REGISTRY.collect()))
