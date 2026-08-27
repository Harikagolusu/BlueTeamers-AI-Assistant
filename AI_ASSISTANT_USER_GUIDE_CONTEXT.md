# BlueTeamers AI Assistant – User Guide Context

| Header | Value |
|---|---|
| **PROJECT** | BlueTeamers AI Assistant — the AI Workspace of the BlueTeamers (InfoSec Dairies) cybersecurity e-learning platform |
| **DOCUMENT PURPOSE** | User-facing feature/context document for Claude to generate the final end-user documentation. Analysis-only; nothing was modified during extraction. |
| **SOURCE** | Local repository snapshot at `~/BlueTeamers-AI-Assistant` (branch `master`). |
| **STATUS** | Complete. All 28 sections below. |

> Classification legend used throughout: **AVAILABLE** = implemented and usable today. **PARTIALLY AVAILABLE** = partially usable or with limitations. **NOT AVAILABLE** = not present. Items that could not be confirmed from the current implementation are explicitly labelled "Not confirmed from the current implementation."

---

## Table of Contents

1. AI Assistant Overview
2. How to Access the AI
3. AI Workspace
4. Starting a Chat
5. Cybersecurity AI Tutor
6. Adaptive Learning / Personalized Responses
7. Course-Aware AI
8. Practice Lab Assistance
9. Wazuh Lab Assistance
10. Cybersecurity Persona
11. Multilingual Support
12. Conversation Memory
13. Chat History
14. Floating AI Assistant
15. Fullscreen AI Workspace
16. Page / Course / Lab Context
17. RAG / Course Material Questions
18. File / Image / PDF Features
19. AI Access Limits
20. Personalized / User-Specific Features
21. Supported Cybersecurity Use Cases
22. Example Questions
23. Good vs Bad Questions
24. User Workflow Examples
25. Troubleshooting for Users
26. User Best Practices
27. Feature Matrix
28. IMPORTANT RESTRICTION

---

# 1. AI ASSISTANT OVERVIEW

The BlueTeamers AI Assistant is a built-in cybersecurity mentor that lives directly inside the **AI Workspace** of the BlueTeamers platform. It is designed for learners of the BlueTeamers cybersecurity courses, and it is always focused on security topics.

It helps users:

- Learn cybersecurity concepts (SOC, SIEM, Blue Team, detection, and more).
- Understand course and lesson material in a conversational way.
- Get help in practice labs and Wazuh labs.
- Analyze logs, events, alerts, IOCs, and detection concepts.
- Receive explanations in the learner's own language (including Telugu and Tinglish).

Unlike normal website content (which is fixed text you read), the AI Workspace is an interactive assistant: you ask questions in your own words, and it gives tailored, step-by-step answers. It adapts to your learning level and to the course you are studying.

---

# 2. HOW TO ACCESS THE AI

There are **two** main ways to reach the AI, and both share the same conversations.

### AI Workspace (`/chat`)

1. **Where the user finds it** — the full AI chat page, opened from the Floating Assistant's "expand" button or directly from the `/chat` route.
2. **What happens when clicked** — a full-page chat workspace opens with a message input, a language selector, and a conversation sidebar.
3. **What the user can do** — start new chats, switch between saved conversations, ask questions, upload files and images, and continue conversations later.

### Floating AI Assistant

1. **Where the user finds it** — a chat button/icon visible on almost every page of the platform.
2. **What happens when clicked** — a small floating chat window opens over the current page without leaving it.
3. **What the user can do** — ask cybersecurity questions while reading a lesson or doing a lab, then close the window and keep working. The floating window can be expanded into the full AI Workspace, and the conversation continues in the same chat thread.

Note: The reading content you see on normal website pages (courses, lessons, articles) is separate from the AI. The AI answers through the assistant, while normal pages are where you read the material.

---

# 3. AI WORKSPACE

Complete user experience:

- **Main chat area** — the central area that shows your messages and the AI's streaming responses.
- **Sidebar** — shows your conversations grouped by time.
- **New Chat** — starts a fresh conversation thread.
- **Conversation History** — previous chats are saved under your account (guests keep only current-session history).
- **Recent Chats** — the most recent conversations are a click away.
- **Conversation switching** — click any saved conversation to open its full history and continue it.
- **Language selector** — choose your response language (Auto Detect, English, Telugu, Tinglish, and more — see Section 11).
- **Message input** — type your question here; press **Enter** to send, **Shift+Enter** for a new line.
- **Send** — the send button dispatches your question (and any attached files/images).
- **Streaming responses** — answers appear progressively as the AI writes them.
- **Upload buttons** — one button for images ("Attach images") and one for files/PDFs ("Attach files or images"); you can also **paste an image with Ctrl/Cmd+V** directly into the message box.
- **Expand/fullscreen** — from the floating assistant, expand to the full workspace.
- **Floating mode** — chat from the small window on any page (see Section 14).

---

# 4. STARTING A CHAT

Step by step:

1. **Open the AI Assistant** — click the floating assistant icon on any page, or open the AI Workspace `/chat`.
2. **Start a new conversation** — click "New Chat" (or just type in the workspace).
3. **Enter a question** — for example: `What is SOC?`
4. **Send it** — press **Enter** or click the send button.
5. **Read the response** — the answer streams in, ready as soon as it appears.
6. **Ask a follow-up question** — for example: `Give me an example.` The AI remembers the context.

Simple cybersecurity examples:

- `What is a SIEM?`
- `Explain Event ID 4625.`
- `Why did this Wazuh alert trigger?`

---

# 5. CYBERSECURITY AI TUTOR

The AI can help users learn and revise the following (all confirmed as supported):

- **Cybersecurity concepts** — general security fundamentals.
- **SOC** — security operations center workflows and analyst tasks.
- **SIEM** — how SIEM platforms work, correlation rules, and log collection (terms like SIEM/SOC/IDS/IPS/firewall/honeypot are always treated as security concepts by the assistant).
- **Blue Team** — defensive security operations.
- **Threat Detection** — detecting suspicious activity.
- **Incident Response** — how to respond to security incidents.
- **Threat Hunting** — actively searching for threats.
- **Log Analysis** — Windows event logs, Linux logs, and general log interpretation.
- **Wazuh** — alerts, rules, and investigation within the Wazuh lab.
- **MITRE ATT&CK** — techniques, tactics, and procedures.
- **Phishing** — detection, analysis, and defense.
- **Malware** — understanding and analyzing malicious software.
- **IOC** — indicators of compromise analysis.
- **CVE** — vulnerability references and understanding.
- **Detection concepts** — detection rules, Sigma/YARA-style rules, and detection engineering.

---

# 6. ADAPTIVE LEARNING / PERSONALIZED RESPONSES

The AI adapts its explanations to the learner:

- **Beginner explanations** — simpler words, more analogies, and basic concepts first.
- **Intermediate explanations** — standard professional detail with technical terms.
- **Advanced / professional explanations** — dense, detailed, and technical.

How it works for the user (in plain language): every time you ask something, the AI quietly considers your level and how you have asked in the past, then chooses the depth of the answer. It also listens for phrases like "I am a beginner" or "give me an expert-level answer" and adjusts immediately.

- Two users asking the same question may receive different explanations — one more basic, one more advanced — because the AI tailors the depth to each learner.
- You can always steer the level yourself: `Explain this in simple words.` or `Give me a professional-level explanation.`

---

# 7. COURSE-AWARE AI

The AI works together with BlueTeamers courses:

- **Enrolled courses** — when you are signed in and enrolled, the AI is aware of your courses.
- **Course context** — it uses your course and lesson context to answer relevant to what you are studying.
- **Lesson context** — while reading a lesson, the AI can use that context when you open the floating assistant.
- **Course material questions** — ask about material from your course.
- **Course-specific answers** — answers can be tailored to the course you are enrolled in.
- **Course suggestions** — the AI can suggest relevant "next" courses or activities when supported.

Example:

- User: "I am studying SIEM. Explain correlation rules."
- The AI uses the SIEM course context to explain correlation rules in a way that fits what the learner is covering.

---

# 8. PRACTICE LAB ASSISTANCE

- **How the AI knows the current lab** — when you are in a practice lab, the AI can pick up the lab context from the page.
- **How users can ask for help** — open the floating assistant inside the lab and ask a question about the current step.
- **How the AI assists without replacing the lab** — the AI gives guidance, hints, and explanations; it does not do the lab for you.
- **Context-aware lab questions** — questions about the current lab receive answers shaped to that lab.
- **Hints/guidance** — the assistant can provide hints designed to keep you learning.
- **Lab-specific assistance** — help for the lab you are actually working in.

Realistic example:

- User (in a practice lab): "I'm stuck on the detection setup in this lab. Give me a hint."
- AI: Offers a step-by-step hint for the current lab step, without giving away the full answer.

---

# 9. WAZUH LAB ASSISTANCE

The AI provides guidance on:

- **Alerts** — understanding why a Wazuh alert triggered and what it means.
- **Logs** — interpreting Wazuh/event logs.
- **Events** — understanding specific events and their significance.
- **Rules** — how Wazuh rules work and what they detect.
- **Investigation** — next steps when investigating an alert.
- **Detection** — detection logic and coverage.
- **Troubleshooting** — common problems in the lab environment.

Example:

- User: "Why did this Wazuh alert trigger?"
- AI: Explains the rule, the event that matched, and what to check next.

---

# 10. CYBERSECURITY PERSONA

From the user's perspective, the assistant behaves like a cybersecurity learning assistant, not a general chatbot:

- **Cybersecurity-focused answers** — answers stay within security/security-ops topics.
- **Technical terminology** — real, correct security terminology is used at an appropriate depth.
- **Relevant explanations** — answers relate to the user's learning path and context.
- **Off-topic handling** — if asked something completely unrelated (e.g. cooking or sports), the AI politely declines and steers back to security topics.
- **Appropriate level of detail** — detail matches the user's level and request.

Examples:

- User: "Tell me a joke about football." → The AI politely declines and re-focuses on cybersecurity topics.
- User: "Explain MITRE ATT&CK." → A proper, structured security explanation.

The assistant also follows a mentor-like, friendly tone while staying technically accurate.

---

# 11. MULTILINGUAL SUPPORT

The language selector offers **24 modes**:

- **Auto Detect** — the AI detects the user's language and responds in that language. It re-detects if the user clearly switches language.
- **English**
- **Indian languages (native script):** Telugu, Hindi, Tamil, Kannada, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia, Urdu
- **Bilingual conversational modes (written in English letters):** Tinglish (Telugu+English), Hinglish (Hindi+English), Tanglish (Tamil+English), Kanglish (Kannada+English), Manglish (Malayalam+English), Banglish (Bengali+English), Marathish (Marathi+English), Gujarlish (Gujarati+English), Punglish (Punjabi+English), Odia-English, Urlish (Urdu+English)

### Auto Detect

The AI identifies the language when someone writes and replies in that same language. If the user clearly switches to another language, the AI re-detects and follows.

### Explicit Language

When the user selects a specific language from the selector, the AI responds in that chosen language regardless of what was written.

### Tinglish

Tinglish is **natural Telugu conversational language written using English letters** — the way Telugu speakers actually type and chat. It is not an artificial Telugu-English word-mixing. Technical terms stay in English, and the conversational flow is natural Telugu using English letters.

Examples the user might type in Tinglish:

- `SIEM ante enti?` (What is a SIEM?)
- `Event ID 4625 enduku triggers avthundi?` (Why does Event ID 4625 trigger?)
- `Wazuh lo alert vaste em cheyyali?` (What should I do when an alert comes in Wazuh?)

The same natural-mixing principle applies to the other bilingual modes (Hinglish, Tanglish, etc.).

---

# 12. CONVERSATION MEMORY

The AI remembers the current conversation so follow-up questions make sense:

- **Follow-up questions** — "Give me an example" or "Explain it more" are understood in context.
- **Previous messages** — earlier messages in the thread are used.
- **Conversation context** — the topic you discussed stays in focus.
- **Session memory** — within a session/thread, the flow of discussion is remembered.

Simple example:

- User: "What is SIEM?"
- AI: Offers an explanation of SIEM.
- User: "Give me an example."
- AI: Understands "it" refers to SIEM and gives a SIEM example.

---

# 13. CHAT HISTORY

- **How conversations are saved** — signed-in users' conversations are saved and appear under their account.
- **How users access previous chats** — from the AI Workspace sidebar.
- **How conversations are named** — titles are generated automatically from the first real question (greeting-only threads keep a generic "New Chat" title).
- **Recent history** — listed in the sidebar (grouped by time: Today / Yesterday / Last 7 Days / Older).
- **History retention** — retained under your account for signed-in users. Guests keep only the current session's short-term context and are not shown in the saved conversation list.
- **Switching conversations** — click a saved conversation to open it.
- **Continuing previous conversations** — the full history loads and you continue exactly where you left off.

---

# 14. FLOATING AI ASSISTANT

- **Floating AI icon** — a chat button shown on nearly every page.
- **Opening the window** — click the icon; a floating chat window opens over the page.
- **Chatting without leaving the current page** — ask questions while reading a lesson or working in a lab, directly in the floating window.
- **Minimizing / closing** — collapse the window back to the icon or close it; the conversation is preserved.
- **Expanding to full AI Workspace** — expand the floating window; it opens the full `/chat` workspace in a new tab with the same conversation continuing.
- **Conversation continuity** — the floating assistant and the full workspace share live chat state, so streaming and history continue seamlessly between them.
- **Page context** — the assistant can use the context of the page you are on (e.g. a SIEM lesson).

Example:

- User reads a SIEM lesson → opens the floating AI → asks a question → gets an answer → closes the AI → continues the lesson.

---

# 15. FULLSCREEN AI WORKSPACE

- **Expand from floating assistant** — the floating window's expand action opens the full workspace in a new tab.
- **`/chat`** — the full AI chat page.
- **Full conversation interface** — a dedicated page with sidebar, history, language selector, and larger chat area.
- **Continuing the same conversation** — the same conversation that was open in the floating assistant continues in the workspace.
- **Returning to floating assistant** — the workspace and floating assistant stay in sync; you can go back and forth without losing the thread.

---

# 16. PAGE / COURSE / LAB CONTEXT

When users ask questions while viewing a supported page, the AI can use the page's available context where implemented:

- **Dashboard** — uses your platform context (courses, progress) where relevant.
- **Course** — understands which course you are viewing.
- **Lesson** — understands which lesson you are reading and can answer about it.
- **Practice Lab** — knows the lab you are in and gives lab-aware guidance.
- **Wazuh Lab** — understands the lab environment and alert investigation.
- **Other supported pages** — page context is provided where implemented.

If page context is not available for a given page, the AI simply answers normally without that context. "Not confirmed from the current implementation" for any specific page not covered above.

---

# 17. RAG / COURSE MATERIAL QUESTIONS

In simple terms: the AI can use relevant BlueTeamers learning material when answering supported questions. When you ask something that matches the platform's course material, the answer can be grounded in that material, so explanations align with the site's content.

Examples:

- "Explain correlation rules according to the SIEM course."
- "What does the Blue Team course say about phishing?"

The AI does not use external/unlisted websites; it works from the platform's own learning material and standard security knowledge.

---

# 18. FILE / IMAGE / PDF FEATURES

What users can actually do today:

### Upload files

- **What can be uploaded** — text-style files: `.txt`, `.log`, `.csv`, `.json`, `.xml`, `.md`, and PDF documents.
- **How to upload** — click the paperclip button ("Attach files or images") and choose one or more files.
- **What the AI does with it** — read the file's contents and incorporate them into its answer (so you can ask about a log file, a JSON config, a document, and so on).
- **Limitations** — up to **5 files** per message; very large files may be rejected (an error will be shown).

### Upload images

- **What can be uploaded** — image files (screenshots, PNG, JPG, and other image formats).
- **How to upload** — click the image button ("Attach images") and choose an image, **or simply paste an image directly into the message box with Ctrl/Cmd+V** (e.g. paste a screenshot right from the clipboard).
- **What the AI does with it** — **AVAILABLE:** the AI reads the text visible in the image (e.g. an error message in a screenshot, a dashboard, event details) and answers based on that text. **PARTIALLY AVAILABLE:** the AI does **not** visually "understand" photos or diagrams as a human would — if an image contains no readable text, it cannot interpret it and will honestly say so and ask you to describe what is in the image.
- **Limitations** — up to **5 images** per message; the AI reads text rather than performing general visual understanding; very large images may be rejected (an error will be shown).

### PDFs

- **What the AI does with it** — documents with a real text layer are read and answered from. **PARTIALLY AVAILABLE:** scanned/image-only PDFs may yield little or no text, because the AI relies on the document's readable text.

---

# 19. AI ACCESS LIMITS

- **Guest users** — can use the AI with a limited daily allowance (no account needed); guests' chats are not saved in the conversation list.
- **Authenticated users** — signed-in users get their own saved history and allowance.
- **Free users** — a free daily limit of **5 AI messages** per day applies by default.
- **Course purchasers / premium** — users who have purchased a BlueTeamers course are treated as premium and get the paid allowance.
- **Message limits** — when the free daily limit is reached, the AI stops answering for the day and shows an upgrade reminder asking you to join/purchase a course to continue.
- **Upgrade/purchase reminder** — the message clearly tells you what to do to get more AI messages.
- **Premium access** — the workspace chat is gated by this allowance; when none remains, the assistant prompts you to upgrade.

The AI does not invent pricing — the exact purchase price shown is whatever the platform presents.

---

# 20. PERSONALIZED / USER-SPECIFIC FEATURES

- **User level** — the AI adapts answer depth to each learner; a visible level selector is "Not confirmed from the current implementation."
- **Enrolled courses** — the AI is aware of the courses you are enrolled in.
- **Course progress** — the AI can consider your progress where supported.
- **Language preference** — your chosen language is remembered for future chats (you can change it anytime in the selector).
- **Conversation history** — your saved chats are yours and load when you return.
- **Memory** — the current conversation's context is remembered (see Section 12).
- **Lab context** — the AI uses the lab you are in when helping you.

---

# 21. SUPPORTED CYBERSECURITY USE CASES

Practical things users can ask the AI (grouped, all implemented):

| Group | Example things to ask |
|---|---|
| Learning | Explain a concept, clarify a lesson, revise a topic |
| SOC | What is a SOC, SOC analyst tasks, SOC workflows |
| SIEM | SIEM basics, correlation rules, log collection |
| Wazuh | Alert explanations, rules, investigation steps |
| Labs | Hints and guidance in the practice/Wazuh labs |
| Logs | Windows event logs, Linux logs, log analysis |
| Threat Hunting | hunt ideas, hunting methodology |
| Incident Response | response steps, IR workflows |
| MITRE ATT&CK | techniques, tactics, mapping |
| Detection | detection rules, Sigma/YARA-style logic |
| Course Questions | questions about your enrolled courses |
| Files/Images | analyze a log file, PDF, or text in a screenshot |

---

# 22. EXAMPLE QUESTIONS

Realistic questions users can ask for each major feature:

- `SIEM ante enti?` (Tinglish — "What is a SIEM?")
- `What is SOC?`
- `Explain this lesson.`
- `Why did this Wazuh alert trigger?`
- `Explain this log.` (with a log file attached, or pasted content)
- `How does this MITRE ATT&CK technique work?`
- `Give me a beginner explanation.`
- `Explain this in Telugu.`
- `Explain this in Tinglish.`
- `Give me a simpler example.`
- `Continue from what we discussed.`
- `I'm studying Windows Event Logs. Explain Event ID 4625.`
- Paste a screenshot with an error and ask: `What does this error mean?`
- Attach a `.log` file and ask: `Any suspicious entries here?`

---

# 23. GOOD VS BAD QUESTIONS

How users can get better results:

| Less effective | More effective |
|---|---|
| `What is 4625?` | `Explain Event ID 4625 for a beginner.` |
| `Is this bad?` | `I'm studying Windows Event Logs. Explain Event ID 4625 and what a SOC analyst should check.` |
| `Explain SIEM.` | `I am studying SIEM. Explain correlation rules with an example.` |
| (no context) | Mention the lesson/course/lab you are working in. |
| `What is this?` | Attach the file/image and say `What is in this log / screenshot?` |

Good communication wins: give a little context, mention your level when needed, and ask clear, specific questions.

---

# 24. USER WORKFLOW EXAMPLES

### Learning

Course → Lesson → AI (floating) → Question → Explanation → Back to lesson

### Lab

Practice Lab → AI → Ask for help → Hint/Guidance → Continue the lab

### Wazuh

Wazuh Lab → Alert → AI → Investigation guidance → Act on the findings

### Follow-up

Question → Answer → Follow-up question → Context-aware next answer

### Floating Assistant

Website page → Floating AI → Question → Answer → Close → Continue activity

### Full Workspace

Floating AI → Expand → `/chat` → Same conversation, full interface → Continue

---

# 25. TROUBLESHOOTING FOR USERS

Simple user-facing solutions:

- **AI not responding** — check your internet connection, wait a moment and try again; if a message is still streaming, press the stop button and ask again.
- **Wrong language** — open the language selector and choose the language you want; the AI will follow it.
- **Conversation not appearing** — make sure you are signed in (guest chats are not saved in the history list); refresh the AI Workspace.
- **Streaming issue** — if the answer stops mid-way, press stop and re-ask, or open the same conversation in the full workspace.
- **Access limit reached** — the daily free limit of 5 messages is used up; the AI will show the upgrade/purchase reminder. New messages renew after the daily reset.
- **Course access issue** — ensure you are signed in and enrolled in the course; course-aware answers require your platform context.
- **Lab context not detected** — open the floating assistant from inside the lab page, or mention the lab name in your question.
- **File/Image upload problem** — make sure the file is a supported type and not too large; re-upload. If you pasted an image and nothing appears, use the image button to pick the file instead.
- **Image with no readable text** — the AI will say it cannot see the image; describe what is shown in words and it will help.

---

# 26. USER BEST PRACTICES

- **Ask specific questions** — specific questions get specific answers.
- **Mention the lesson/topic when needed** — helps the AI use course/lab context.
- **Ask follow-up questions** — build understanding step by step.
- **Use language selection** — pick your preferred language once; the AI remembers it.
- **Use the floating assistant while learning** — get help without leaving the lesson.
- **Ask for simpler explanations** — say `Explain in simple words` for a beginner version.
- **Ask for examples** — the AI gives great worked examples.
- **Use lab context** — ask from inside the lab so the AI knows what you are working on.
- **Upload instead of describing** — for logs/screener text, attach the file or paste the image so the AI reads the exact content.

---

# 27. FEATURE MATRIX

| Feature | User Can Use? | How to Access | Short Description |
|---|---|---|---|
| AI Workspace (`/chat`) | AVAILABLE | Floating assistant → expand, or `/chat` | Full-page AI chat with history and language selector |
| Floating AI Assistant | AVAILABLE | Chat icon on almost every page | Chat without leaving the current page |
| New Chat | AVAILABLE | "New Chat" in the workspace | Start a fresh conversation |
| Conversation History | AVAILABLE | Workspace sidebar | Saved chats under your account |
| Continue a conversation | AVAILABLE | Click a saved conversation | Pick up exactly where you left off |
| Language selector (24 modes) | AVAILABLE | Selector above the message box | Auto/English/Indian languages/bilingual modes |
| Auto-detect language | AVAILABLE | Choose "Auto Detect" | Replies in the user's language |
| Streaming responses | AVAILABLE | Any chat | Answers appear progressively |
| Course-aware answers | PARTIALLY AVAILABLE | Chat while signed in / enrolled | Uses enrolled courses & lesson context |
| Practice Lab guidance | AVAILABLE | Floating assistant inside a lab | Lab-aware hints and guidance |
| Wazuh Lab assistance | AVAILABLE | Floating assistant inside the Wazuh lab | Alerts, rules, logs, investigation help |
| Adaptive learner level | AVAILABLE | No setup needed | Explanations match your level; you can also request depth in words |
| Upload files (.txt/.log/.csv/.json/.xml/.md/.pdf) | AVAILABLE | Paperclip button on the message box | AI reads and answers from the file's contents |
| Upload images | AVAILABLE | Image button, or Ctrl/Cmd+V paste | AI reads text visible in the image |
| Image visual understanding (photos/diagrams) | PARTIALLY AVAILABLE | Attach an image | Cannot "see" as a human; reads readable text, else asks for a description |
| PDF reading | AVAILABLE | Paperclip button (PDF) | Reads text-layer PDFs |
| Import access limit (5/day free) | AVAILABLE | Automatic | Free daily allowance, upgrade reminder after |
| Conversation memory | AVAILABLE | Follow-ups in a thread | Understands "it" and prior context |
| Platform context (courses/progress) | AVAILABLE | Signed-in chats | Uses your BlueTeamers account context |
| Off-topic handling | AVAILABLE | Any chat | Politely declines non-security topics |

---

# 28. IMPORTANT RESTRICTION

Do not describe internal architecture in the final user guide. Do not include:

- Python classes
- API implementation details
- Database schema
- Internal services
- Prompt builders
- Internal stage names
- Internal model names
- Environment variables
- API keys
- Developer configuration

Those belong in the technical documentation.

Everything here is described from the user's point of view — what the learner can do, click, and expect.

---

# OUTPUT

This document is the complete user-guide context, with simple explanations, step-by-step instructions, tables, examples, workflows, and feature lists, and it does not modify or describe the internals of the codebase.

## Summary — results of the review

### 1. Features confirmed available
- AI Workspace `/chat` and the Floating AI Assistant, with shared live conversation state.
- New chats, saved conversation history (signed-in users), auto titles, and conversation switching.
- Streaming answers, message input, send, and stop.
- Language selector with 24 modes including Auto Detect, English, 11 Indian languages, and 11 bilingual modes; Tinglish as natural Telugu written in English letters.
- Conversation memory for follow-up questions.
- Course-aware and lab-aware answers; practice lab and Wazuh lab assistance.
- Cybersecurity tutor across SOC, SIEM, Blue Team, threat detection, incident response, threat hunting, log analysis, MITRE ATT&CK, phishing, malware, IOC, CVE, detection.
- Adaptive learner-level explanations.
- File uploads (`.txt/.log/.csv/.json/.xml/.md/.pdf`) — AI reads their contents.
- Image uploads via the image button and via Ctrl/Cmd+V paste — AI reads text visible in the image.
- Text-layer PDF reading.
- Free daily allowance (5 messages) with an upgrade/purchase reminder; premium access via course purchase.

### 2. Features partially available
- General visual understanding of images: the AI reads text but cannot interpret photos/diagrams that contain no readable text (it says so and asks for a description).
- Scanned/image-only PDFs may yield little or no text.
- Course-aware answers depend on the user being signed in and enrolled (guest chats carry less platform context).

### 3. Features not confirmed
- "Not confirmed from the current implementation": a user-visible learner-level selector.
- "Not confirmed from the current implementation": any general vision/multimodal image understanding (the assistant is text/OCR based).
- "Not confirmed from the current implementation": the exact daily reset time shown to end users.
- "Not confirmed from the current implementation": the exact server error wording for network/storage failures.

### 4. Any user-facing limitations
- Free daily limit of 5 AI messages (upgrade/purchase required to continue).
- Up to 5 files and up to 5 images per message; very large uploads may be rejected.
- Images: readable text is extracted; non-text images cannot be "seen".
- Image-only PDFs may return little content.
- Guest usage is limited and not saved to the conversation history list.
- Responses are cybersecurity-focused; off-topic requests are politely declined.

### 5. Files / components inspected
- `infosecdairies/src/components/ai/FloatingAssistant.tsx` — floating chat window, expansion, page context, attachments.
- `infosecdairies/src/components/ui/Chat.tsx` — full workspace chat surface.
- `infosecdairies/src/components/ui/chat/ChatInput.tsx` — message input, image/file upload buttons, Ctrl/Cmd+V paste, language selector.
- `infosecdairies/src/components/ui/chat/WorkspaceSidebar.tsx` — conversation history/sidebar UI.
- `ai_service/app/chat/pipeline/stages` — pipeline stages for language, memory, attachments (image/PDF parsing), platform context, persona, persistence. (Referenced for behavior verification only; not surfaced in the guide.)
- Language catalog and adaptive-level configuration (behavior verified; not surfaced in the guide).
- API request validation keys (attachment/query limits verified; not surfaced in the guide).
- Freemium access-control behavior (daily limit and upgrade reminder verified; not surfaced in the guide).