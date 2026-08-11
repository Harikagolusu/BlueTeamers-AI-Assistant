# Frontend-Backend Integration Architecture

## Overview
BlueTeamers AI Assistant integrates a React/Vite SPA with a FastAPI backend driven by an advanced orchestration engine.

## Components
- **Frontend (React)**: ChatUI, SSE Hooks, Markdown rendering.
- **Backend (FastAPI)**: /api/chat/ endpoint utilizing Dependency Injection to swap between Dummy and Real services.
- **Bootstrap Layer**: Resolves Ollama, Redis Memory, and FAISS RAG dependencies.
- **Ollama Engine**: Local execution of qwen2.5:7b.
