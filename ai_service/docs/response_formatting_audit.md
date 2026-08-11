# Response Formatting Audit

This document contains the audit of the response rendering pipeline in the BlueTeamers AI Assistant to isolate the root cause of collapsed formatting and unrendered Markdown.

## Pipeline Analysis & Findings

We traced a markdown payload (containing headings, newlines, code fences, and bullet points) through each segment of the delivery pipeline:

```
Ollama Server (Returns raw markdown)
         │
         ▼
LLM Provider / OllamaProvider (Extracts "response" token)
         │
         ▼
ChatService / _stream_response (Wraps tokens in SSE format)
         │
         ▼
HTTP Network (Delivers event-stream chunks)
         │
         ▼
Frontend useChat Hook (Splits chunk by \n, decodes token)
         │
         ▼
React Chat Component (Renders <ReactMarkdown> inside container)
```

### 1. Ollama Server & LLM Provider (Backend Source)
- **Status**: **PASS**
- **Finding**: Ollama returns raw token streams containing correct markdown characters (`#`, `-`, `\n`, etc.). No cleaning functions or regex patterns in `OllamaProvider` strip these tokens.

### 2. SSE Stream Serialization (`app/chat/service.py`)
- **Status**: **FAIL** (Root Cause 1)
- **Finding**: The server was formatting streaming tokens as `data: {chunk}\n\n`. When the LLM yielded a newline token (`\n`), it resulted in `data: \n\n\n`. In Server-Sent Events, double newlines demarcate the end of a message event. The newline token was being parsed as an empty message boundary.
- **Resolution**: Refactored the stream writer to serialize tokens as structured JSON payloads (`data: {"token": "\n"}\n\n`). JSON serialization escapes newlines (`\n` -> `\n`) and preserves them across network boundaries.

### 3. Frontend Stream Parsing (`useChat.ts`)
- **Status**: **PASS** (Compatible)
- **Finding**: The frontend parsing logic already contained structured JSON token parsing support (`const parsed = JSON.parse(data); if (parsed.token) { lastMsg.content += parsed.token; }`). By changing the backend payload format to match this JSON schema, the stream parser now correctly restores all formatting, whitespace, and newlines.

### 4. Frontend Markdown Styling (`tailwind.config.ts`)
- **Status**: **FAIL** (Root Cause 2)
- **Finding**: The Chat UI wrapped the `<ReactMarkdown>` component with Tailwind typography classes (`prose prose-sm dark:prose-invert`). However, the `@tailwindcss/typography` plugin was not registered in `tailwind.config.ts`. As a result, the browser applied no styling to markdown headings, tables, bullet points, blockquotes, or code fences, rendering them as raw, collapsed plain text.
- **Resolution**: Registered `require("@tailwindcss/typography")` in the plugins array of `tailwind.config.ts`. This instantly restores standard styling to all markdown elements.
