<USER_REQUEST>
# BlueTeamers AI Assistant - Final Development Sprint
# Master Implementation Prompt

# Goal

The project is approximately 90% complete.

The backend architecture, PlatformAgentOrchestrator, multi-agent framework, RAG pipeline, runtime hardening, frontend integration, and local Ollama deployment are already implemented.

The objective of this sprint is NOT to redesign the system.

The objective is to complete the remaining platform capabilities exactly according to the approved architecture while preserving all existing work.

This sprint should transform the project into a production-quality AI Cybersecurity Assistant suitable for demonstration.

---

# IMPORTANT

Before making ANY code changes,

perform a complete architectural audit.

Understand the existing implementation.

Do NOT duplicate features.

Do NOT rebuild existing modules.

Reuse the current implementation wherever possible.

Follow the existing architecture.

---

# Architecture Rules

Preserve:

- PlatformAgentOrchestrator
- WorkflowBuilder
- QueryRouter
- CapabilityRegistry
- AgentRegistry
- ToolRegistry
- LLMFactory
- Dependency Injection
- ExecutionScheduler
- WorkerPool
- ExecutionHistory
- Runtime Diagnostics
- PlatformBootstrapper

Do NOT redesign any of these.

Extend them only where necessary.

---

# Development Rules

For every completed task

1. Run affected tests.
2. Validate functionality.
3. Update

```
docs/daily_logs/today_work.md
```

4. Update

```
docs/daily_logs/change_log.md
```

Never complete multiple features without validation.

Work incrementally.

---

# FEATURE 1
## Intelligent Query Router

Current issue:

Some requests incorrectly enter the RAG pipeline.

Restore the intended routing architecture.

The router must classify requests into:

- GENERAL_CHAT
- RAG_CHAT
- TOOL_CHAT
- IMAGE_CHAT
- DOCUMENT_CHAT
- LAB_ASSISTANT
- INVESTIGATION

Examples

Hello

↓

GENERAL_CHAT

Who are you?

↓

GENERAL_CHAT

Explain MITRE ATT&CK

↓

RAG_CHAT

Analyze this log

↓

INVESTIGATION

Summarize this PDF

↓

DOCUMENT_CHAT

Analyze this screenshot

↓

IMAGE_CHAT

Search CVE-2024-12345

↓

TOOL_CHAT

Validate every route.

---

# FEATURE 2
## Multi-Agent Collaboration

Improve the orchestrator.

Allow multiple agents to collaborate.

Example

User

↓

Knowledge Assistant

↓

Investigation Agent

↓

Learning Coach

↓

Aggregator

↓

Final Response

Maintain execution trace.

---

# FEATURE 3
## Conversation Memory

Implement

Short-term memory

Long-term memory

Remember

conversation

learning progress

previous questions

weak topics

assessment history

preferred learning path

Ensure memory works across sessions where applicable.

---

# FEATURE 4
## RAG Enhancement

Audit current RAG.

Improve

retrieval

ranking

chunk selection

prompt construction

source attribution

Support

MITRE

OWASP

NIST

Sigma

YARA

custom documents

Display retrieved sources.

---

# FEATURE 5
## Document Upload

Implement

PDF Upload

Word Upload

Text Upload

Pipeline

Upload

↓

Parser

↓

Chunking

↓

Embeddings

↓

Vector Store

↓

RAG

↓

LLM

Support conversational querying.

---

# FEATURE 6
## Image Understanding

Integrate vision capability.

Support

screenshots

incident images

architecture diagrams

SOC dashboards

phishing emails

security reports

Route image requests automatically.

Use the vision provider configured for Ollama.

Do NOT replace the text LLM.

---

# FEATURE 7
## Log Analysis

Support

Windows Logs

Sysmon

Apache

Nginx

Firewall

Suricata

Zeek

Output

Summary

Timeline

MITRE Mapping

Threat Analysis

Recommendations

---

# FEATURE 8
## Agent Visibility

Frontend must display

Active Agent

Agent Chain

Execution Steps

Response Sources

Execution Time

Confidence

This should help demonstrate the orchestration.

---

# FEATURE 9
## Citation Panel

Display

Retrieved Documents

Knowledge Source

Chunk

Similarity Score

Reference Links

Confidence

Support expandable citations.

---

# FEATURE 10
## Learning Intelligence

Implement

Skill Tracking

Weak Topics

Strong Topics

Learning Trend

SOC Readiness

Assessment Progress

Store history.

---

# FEATURE 11
## Recommendation Engine

Recommend

Next Topic

Next Lab

Next Course

Next MITRE Technique

Certification

Weekly Learning Plan

Generate recommendations from memory.

---

# FEATURE 12
## Streaming Improvements

Improve

token streaming

markdown rendering

tables

lists

code blocks

syntax highlighting

Ensure responses appear naturally.

---

# FEATURE 13
## UI Improvements

Modernize the chat UI.

Include

chat history

attachments

markdown

copy button

code formatting

agent badges

citation panel

streaming indicator

typing indicator

memory indicator

theme consistency

---

# FEATURE 14
## Dashboard

Display

Recent Conversations

Learning Progress

Statistics

Recommendations

Recent Documents

Recent Investigations

Recent Assessments

---

# FEATURE 15
## Runtime Analytics

Collect

Latency

Execution Time

Tokens

Retrieved Documents

Agent Used

LLM Used

Memory Hits

Tool Calls

Display these in diagnostics.

---

# FEATURE 16
## Security

Implement

Prompt Injection Detection

PII Detection

Output Validation

Guardrails

Unsafe Prompt Detection

Maintain existing security architecture.

---

# FEATURE 17
## Demo Mode

Provide

Development Demo Mode

without changing production authentication.

Support

demo user

demo data

demo conversation

development flag

---

# FEATURE 18
## Local Deployment

Verify

Frontend

Backend

Ollama

Vector Store

Embeddings

All launch successfully.

Update startup scripts.

---

# FEATURE 19
## Documentation

Generate

architecture updates

API documentation

deployment guide

demo guide

demo questions

known limitations

feature inventory

system workflow

runtime workflow

agent workflow

RAG workflow

memory workflow

---

# FEATURE 20
## Final Validation

Run

pytest

integration tests

runtime tests

manual validation

Verify

General Chat

↓

LLM

Cybersecurity Question

↓

RAG

↓

LLM

Image

↓

Vision Model

Document

↓

RAG

Tool Request

↓

Tool Execution

Log Analysis

↓

Investigation Agent

Everything must work from the React UI.

---

# Constraints

Do NOT

- rewrite architecture
- remove modules
- duplicate implementations
- hardcode responses
- bypass QueryRouter
- bypass PlatformAgentOrchestrator
- bypass LLMFactory
- bypass RAG
- bypass Dependency Injection

Reuse existing components.

Only extend where necessary.

---

# Deliverables

Generate

- Feature completion report
- Architecture update report
- Demo readiness report
- Production readiness report
- UI feature inventory
- Backend feature inventory
- Runtime validation report
- End-to-end validation report

Update

docs/daily_logs/today_work.md

docs/daily_logs/change_log.md

after every completed feature.

---

# Success Criteria

The sprint is complete only when:

- All core features described in the architecture are implemented or explicitly documented if deferred.
- General chat, RAG, document analysis, image analysis, log analysis, and tool execution all work from the React UI.
- QueryRouter correctly classifies requests.
- PlatformAgentOrchestrator coordinates multi-agent workflows.
- Memory, recommendations, and citations are functional.
- Local deployment works with Ollama.
- The project is fully demo-ready with a clean, maintainable architecture.
</USER_REQUEST>
<ADDITIONAL_METADATA>
The current local time is: 2026-08-03T15:16:42+05:30.

The user's current state is as follows:
Active Document: c:\Users\golus\Desktop\BlueTeamers-AI-Assistant\ai_service\docs\daily_logs\today_work.md (LANGUAGE_MARKDOWN)
Cursor is on line: 201
Other open documents:
- c:\Users\golus\Desktop\BlueTeamers-AI-Assistant\ai_service\app\integrations\certificates_api.py (LANGUAGE_PYTHON)
- c:\Users\golus\Desktop\BlueTeamers-AI-Assistant\infosecdairies\infosec-backend\backend\leads\urls.py (LANGUAGE_PYTHON)
- c:\Users\golus\Desktop\BlueTeamers-AI-Assistant\start_all.bat (LANGUAGE_UNSPECIFIED)
- c:\Users\golus\Desktop\BlueTeamers-AI-Assistant\ai_service\docs\daily_logs\today_work.md (LANGUAGE_MARKDOWN)
- c:\Users\golus\Desktop\BlueTeamers-AI-Assistant\ai_service\.env (LANGUAGE_UNSPECIFIED)
</ADDITIONAL_METADATA>
<USER_SETTINGS_CHANGE>
The user changed setting `Model Selection` from  to Gemini 3.1 Pro (High). No need to comment on this change if the user doesn't ask about it. If reporting what model you are, please use a human readable name instead of the exact string.
</USER_SETTINGS_CHANGE>