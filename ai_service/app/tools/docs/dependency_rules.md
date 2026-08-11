# Dependency Rules

The Enterprise Tool Library strictly adheres to Clean Architecture. Dependencies point strictly inwards toward the Domain Layer. This is mathematically enforced by our architecture tests suite.

| Layer | May Depend On | Description |
|---|---|---|
| **Domain** | **Nothing** | The innermost layer containing pure business models, entities (e.g. `SearchDocument`, `MitreTechnique`), Request/Response DTO schemas, and metadata structures. Must have absolutely no knowledge of outside frameworks, databases, JSON protocols (e.g. STIX), or API providers. |
| **Application** | **Domain + Interfaces** | The orchestration layer. Defines the Interfaces (`IUtilityService`, `ISearchService`) and provides business implementations that consume those interfaces. May reference Domain models. Must never directly import concrete implementations (like `FAISSProvider`). |
| **Infrastructure** | **Interfaces + External SDKs** | Contains concrete implementations of interfaces (e.g., the actual HTTP calls to VirusTotal, or FAISS library bindings). Includes observability, factory patterns, and response building. May depend on Application interfaces and Domain models. |
| **Implementations** | **Application Interfaces + Domain** | The entry points. These are the thin Tool classes decorated with `@tool`. They receive the raw `ToolRequest`, trigger Pydantic schema validation, and invoke the Application layer. They must never directly invoke Infrastructure components (providers). |

## Rule Enforcement

These boundary rules are continuously monitored in CI via:
`tests/tools/architecture/test_architecture.py`

If you inadvertently import an Infrastructure concrete class into the Domain, the build will fail immediately.
