# Enterprise Tool Library Architecture

This diagram illustrates the high-level architecture of the Tool Execution flow, demonstrating the Clean Architecture layers and dependency inversion principles.

```mermaid
flowchart TD
    %% Define styles
    classDef llm fill:#f9f,stroke:#333,stroke-width:2px
    classDef entry fill:#bbf,stroke:#333,stroke-width:2px
    classDef implementation fill:#bfb,stroke:#333,stroke-width:2px
    classDef application fill:#fbf,stroke:#333,stroke-width:2px
    classDef interface fill:#ffb,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    classDef provider fill:#fbb,stroke:#333,stroke-width:2px
    classDef domain fill:#eee,stroke:#333,stroke-width:2px
    classDef response fill:#ddd,stroke:#333,stroke-width:2px

    %% Nodes
    LLM("LLM (Agent / System)"):::llm
    Executor("Tool Executor (Module 2)"):::entry
    Tool("Tool Implementation (e.g. VectorSearchTool)"):::implementation
    AppService("Application Service (e.g. SearchApplicationService)"):::application
    IProvider("Provider Interface (e.g. ISearchProvider)"):::interface
    Provider("Provider Implementation (e.g. MockSearchProvider)"):::provider
    DomainModel("Domain Model (e.g. SearchDocument)"):::domain
    Builder("ResponseBuilder"):::response

    %% Flow
    LLM -->|"1. Decides to call tool"| Executor
    Executor -->|"2. Invokes execute()"| Tool
    Tool -->|"3. Orchestrates request"| AppService
    AppService -->|"4. Calls interface method"| IProvider
    IProvider -.->|"5. Implemented by"| Provider
    Provider -->|"6. Fetches data & returns"| DomainModel
    AppService -->|"7. Returns Result"| Tool
    Tool -->|"8. Formats response"| Builder
    Builder -->|"9. Returns ToolResponse"| Executor
    Executor -->|"10. Returns to"| LLM

    %% Layer groupings
    subgraph "Entry Point"
        LLM
        Executor
    end

    subgraph "Implementation Layer"
        Tool
    end

    subgraph "Application Layer"
        AppService
    end

    subgraph "Infrastructure Layer"
        IProvider
        Provider
        Builder
    end

    subgraph "Domain Layer"
        DomainModel
    end
```
