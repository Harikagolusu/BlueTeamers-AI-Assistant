import { useState, useRef, useCallback, useEffect } from 'react';
import { apiUrl } from '../services/api';
import type { PageContextPayload } from '../lib/pageContext';
import { getGuestId } from '../lib/guestId';

const SESSION_STORAGE_KEY = 'bt_chat_messages_v1';
const CONVERSATION_ID_STORAGE_KEY = 'bt_chat_conversation_id_v1';
const LANGUAGE_STORAGE_KEY = 'bt_chat_language_v1';

// Cross-tab conversation sync channel. sessionStorage is PER-TAB, so the
// floating assistant and the /chat workspace only share a conversation when
// they live in the SAME tab. The "Open full workspace" button opens a NEW tab,
// so we additionally mirror chat state over a BroadcastChannel: changes in one
// tab replay live into the other, and a freshly-opened workspace pulls the
// in-flight conversation from the floating window.
const SYNC_CHANNEL = 'bt_chat_sync_v1';

function safeRandomUUID(): string {
  try {
    if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
      return crypto.randomUUID();
    }
  } catch {
    // ignore and fall back
  }
  return `r-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

interface SyncState {
  messages: ChatMessage[];
  conversationId: string | null;
}

const signatureOf = (m: ChatMessage[]) => JSON.stringify(m);

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  metadata?: any;
}

export interface ChatError {
  message: string;
  status?: number;
  code?: string;
  access?: unknown;
}

export function useChat(onNewConversation?: (id: string) => void) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [errorDetail, setErrorDetail] = useState<ChatError | null>(null);
  // Resume the active conversation across surfaces and page reloads: any fresh
  // useChat instance (workspace or floating assistant) starts on the SAME
  // conversation id stored for an in-progress session, so messages keep
  // grouping into one conversation until the user explicitly starts a new chat.
  const [conversationId, setConversationId] = useState<string | null>(() => {
    try {
      const saved = sessionStorage.getItem(SESSION_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.some((m: ChatMessage) => m && m.role === 'user')) {
          return sessionStorage.getItem(CONVERSATION_ID_STORAGE_KEY);
        }
      }
    } catch {
      // unavailable/corrupt storage -> start fresh.
    }
    return null;
  });
  // Ref so sendMessage (stable [] callback) always sees the latest id.
  const conversationIdRef = useRef<string | null>(null);
  useEffect(() => {
    conversationIdRef.current = conversationId;
  }, [conversationId]);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Cross-tab BroadcastChannel sync (see SYNC_CHANNEL comment). Each useChat
  // instance mirrors { messages, conversationId } to sibling tabs so the
  // floating window and the full workspace continue the same LIVE conversation
  // even when the workspace is opened in a new tab (sessionStorage is per-tab,
  // so a new tab would otherwise start empty and never receive updates).
  const instanceIdRef = useRef<string>(`bt-chat-${safeRandomUUID()}`);
  const channelRef = useRef<BroadcastChannel | null>(null);
  // Hash of the last snapshot this instance announced (or adopted) so we never
  // echo identical state back and forth between tabs.
  const lastPublishedHashRef = useRef<string | null>(null);
  // Skip the very first publish: a freshly-opened tab must PULL the in-flight
  // conversation (REQUEST) rather than announce an empty state that could wipe
  // a live conversation held by the floating window.
  const skipFirstPublishRef = useRef(true);
  // While a REQUEST for another tab's conversation is outstanding, publishing is
  // suppressed: this tab must ADOPT existing state (sibling -> this) before it
  // may announce anything back, otherwise its initial default welcome would
  // clobber the live conversation in the floating window. Cleared once state is
  // adopted, or after a short grace period when no sibling holds a conversation.
  const adoptionPendingRef = useRef(false);
  const adoptionTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  // Ref mirror of messages so the channel handler (registered once) and the
  // in-flight initializeSession always read the current value.
  const messagesRef = useRef<ChatMessage[]>(messages);
  useEffect(() => {
    messagesRef.current = messages;
  }, [messages]);

  const applyIncomingState = useCallback((data: SyncState & { instanceId?: string; fromClear?: boolean }) => {
    const incoming = data.messages;
    const incomingId = data.conversationId ?? null;
    if (!Array.isArray(incoming)) return;
    // Adopting a sibling's state ends our request/wait for adoption.
    adoptionPendingRef.current = false;
    const localMessages = messagesRef.current;
    const localId = conversationIdRef.current;

    // Only an explicit CLEAR may wipe a live conversation; a stray empty
    // snapshot (e.g. an uninitialized sibling tab) must not clobber history.
    if (incoming.length === 0 && localMessages.length > 0 && !data.fromClear) return;

    const sameMessages = signatureOf(localMessages) === signatureOf(incoming);
    const sameId = localId === incomingId;
    if (sameMessages && sameId) return;

    // Mark the adopted snapshot as already-announced so we don't echo it back.
    lastPublishedHashRef.current = JSON.stringify({ m: incoming, c: incomingId });
    setMessages(incoming);
    if (!sameId) setConversationId(incomingId);
  }, []);

  const applyIncomingRef = useRef(applyIncomingState);
  useEffect(() => {
    applyIncomingRef.current = applyIncomingState;
  }, [applyIncomingState]);

  // Subscribe to the sync channel. A freshly-opened workspace tab has EMPTY
  // sessionStorage, so it broadcasts a REQUEST and adopts the in-flight
  // conversation from whichever tab holds it (usually the floating window).
  useEffect(() => {
    let channel: BroadcastChannel | null = null;
    try {
      channel = new BroadcastChannel(SYNC_CHANNEL);
      channelRef.current = channel;
    } catch {
      return; // BroadcastChannel unsupported -> same-tab + sessionStorage only
    }

    channel.onmessage = (ev: MessageEvent) => {
      const data = ev.data;
      if (!data || typeof data !== 'object' || data.instanceId === instanceIdRef.current) return;
      if (data.type === 'request') {
        // Another tab just opened and wants our current conversation.
        const state: SyncState = {
          messages: messagesRef.current,
          conversationId: conversationIdRef.current,
        };
        if (state.messages.length > 0 || state.conversationId) {
          try {
            channelRef.current?.postMessage({
              type: 'state',
              instanceId: instanceIdRef.current,
              ...state,
            });
          } catch {
            // best-effort
          }
        }
        return;
      }
      if (data.type === 'clear') {
        // A sibling tab explicitly cleared / started a new conversation.
        adoptionPendingRef.current = false;
        if (messagesRef.current.length === 0 && conversationIdRef.current === data.conversationId) return;
        lastPublishedHashRef.current = null;
        setMessages([]);
        setConversationId(data.conversationId ?? null);
        return;
      }
      if (data.type === 'state') {
        applyIncomingRef.current(data);
      }
    };

    // Only ask for another tab's conversation when this tab has nothing of its
    // own to resume (fresh open) — never clobber a restored session.
    let hasSavedConversation = false;
    try {
      const saved = sessionStorage.getItem(SESSION_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        hasSavedConversation =
          Array.isArray(parsed) && parsed.some((m: ChatMessage) => m && m.role === 'user');
      }
    } catch {
      // best-effort
    }
    if (!hasSavedConversation && messagesRef.current.length === 0) {
      adoptionPendingRef.current = true;
      try {
        channel.postMessage({ type: 'request', instanceId: instanceIdRef.current });
      } catch {
        // best-effort
      }
      // If no sibling tab holds a conversation, stop waiting shortly so this
      // tab's own fresh welcome can be announced normally.
      adoptionTimeoutRef.current = setTimeout(() => {
        adoptionPendingRef.current = false;
      }, 350);
    }

    return () => {
      channelRef.current = null;
      if (adoptionTimeoutRef.current) {
        clearTimeout(adoptionTimeoutRef.current);
        adoptionTimeoutRef.current = null;
      }
      try {
        channel?.close();
      } catch {
        // best-effort
      }
    };
  }, []);

  // Response language (Sprint 7): default Auto Detect, persisted locally and
  // synced to the authenticated user's server-side preference.
  const [language, setLanguageState] = useState<string>(() => {
    try {
      return localStorage.getItem(LANGUAGE_STORAGE_KEY) || 'auto';
    } catch {
      return 'auto';
    }
  });
  const languageRef = useRef<string>(language);
  useEffect(() => {
    languageRef.current = language;
  }, [language]);
  // True only when the user actively changed the language via the selector in
  // this session. A remembered preference auto-loaded into the dropdown must
  // NOT be re-sent as an explicit request field: the backend treats an explicit
  // code as a hard manual override and skips auto-detection (so e.g. a Tinglish
  // query would be forced back into pure Telugu). Leaving it out lets the
  // backend apply its own stored-preference + detection-override logic.
  const languageToggledRef = useRef(false);

  // Load the authenticated user's remembered language preference once, unless
  // a local override already exists (local wins within this browser).
  useEffect(() => {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) return;
    try {
      if (localStorage.getItem(LANGUAGE_STORAGE_KEY)) return;
    } catch {
      // best-effort
    }
    fetch(apiUrl('/api/language/preference'), {
      headers: { Authorization: `Bearer ${accessToken}` },
    })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && data.language && data.language !== 'auto') {
          setLanguageState(data.language);
          try {
            localStorage.setItem(LANGUAGE_STORAGE_KEY, data.language);
          } catch {
            // best-effort
          }
        }
      })
      .catch(() => {
        // server preference is best-effort; detection still applies
      });
  }, []);

  const setLanguage = useCallback((code: string) => {
    setLanguageState(code);
    languageToggledRef.current = true;
    try {
      localStorage.setItem(LANGUAGE_STORAGE_KEY, code);
    } catch {
      // best-effort
    }
    // Persist to the backend so future conversations keep the same language.
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) return;
    fetch(apiUrl('/api/language/preference'), {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ language: code }),
    }).catch(() => {
      // best-effort
    });
  }, []);

  // Persist the conversation so navigating away (e.g. to a course via a
  // Course Source Card) and pressing Browser Back restores it exactly.
  useEffect(() => {
    try {
      sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(messages));
    } catch {
      // sessionStorage may be unavailable; persistence is best-effort.
    }
  }, [messages]);

  // Persist the conversation id so the floating assistant and the /chat
  // workspace continue the same conversation across both surfaces.
  useEffect(() => {
    if (conversationId) {
      try {
        sessionStorage.setItem(CONVERSATION_ID_STORAGE_KEY, conversationId);
      } catch {
        // best-effort
      }
    }
  }, [conversationId]);

  // Mirror local chat state to sibling tabs (live updates in both directions).
  // The first render is skipped for a freshly-opened tab so it pulls via
  // REQUEST instead of announcing an empty state.
  useEffect(() => {
    if (skipFirstPublishRef.current) {
      skipFirstPublishRef.current = false;
      // A restored tab (saved conversation id from sessionStorage) should still
      // announce itself rather than sit silently.
      if (messages.length === 0 && !conversationId) return;
    }
    // Pending a REQUEST response: adopt before announcing, or the default
    // welcome seeded by initializeSession could clobber the live conversation.
    if (adoptionPendingRef.current) return;
    const hash = JSON.stringify({ m: messages, c: conversationId });
    if (lastPublishedHashRef.current === hash) return;
    lastPublishedHashRef.current = hash;
    try {
      channelRef.current?.postMessage({
        type: 'state',
        instanceId: instanceIdRef.current,
        messages,
        conversationId,
      });
    } catch {
      // best-effort
    }
  }, [messages, conversationId]);

  // Core streaming helper shared by normal sends and the silent lab-hint send.
  const streamChat = useCallback(async (
    payload: any,
    onEvent: (ev: { token?: string; metadata?: any }) => void,
  ) => {
    // Abort previous request if still running
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    const accessToken = localStorage.getItem("accessToken");
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    if (accessToken) {
      headers['Authorization'] = `Bearer ${accessToken}`;
    }

    const response = await fetch(apiUrl('/api/chat/'), {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
      signal: abortControllerRef.current.signal,
    });

    if (!response.ok) {
      // Surface structured errors (e.g. HTTP 429 free_ai_limit_reached) so the
      // UI can react to them (show an upgrade dialog) instead of a raw status.
      const err: ChatError = new Error(`Error: ${response.status} ${response.statusText}`);
      err.status = response.status;
      try {
        const body = await response.json();
        if (body && typeof body === 'object') {
          const detail = body.detail;
          if (typeof detail === 'string') {
            err.message = detail;
          } else if (detail && typeof detail === 'object') {
            err.message = detail.message || err.message;
            err.code = detail.code;
            err.access = detail.access;
          }
        }
      } catch {
        // Non-JSON error body — keep the default status message.
      }
      throw err;
    }

    if (!response.body) {
      throw new Error("No response body");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let done = false;

    // Basic SSE parsing logic (very simplified for this demo)
    // The backend yields text/event-stream chunks. Complete SSE lines are
    // processed one at a time, while a partial trailing line is kept in the
    // buffer until the next read. This prevents a large metadata event that
    // gets split across TCP reads from being appended to the message content
    // as raw JSON text.
    const handleLine = (rawLine: string): boolean => {
      const line = rawLine.replace(/\r$/, '');
      if (line.startsWith('data: ')) {
        const data = line.slice(6);
        if (data === '[DONE]') {
          return true;
        }
        try {
          // If it's a JSON payload (e.g. streaming tokens or metadata)
          const parsed = JSON.parse(data);
          if (parsed.token !== undefined || parsed.metadata !== undefined) {
            onEvent({ token: parsed.token, metadata: parsed.metadata });
          }
        } catch (e) {
          // Not JSON, might just be raw text if the backend sends raw tokens
          onEvent({ token: data });
        }
      } else if (line.trim().length > 0 && !line.startsWith('event:') && !line.startsWith('id:')) {
        // If the backend isn't sending standard SSE but just raw chunked text
        onEvent({ token: line });
      }
      return false;
    };

    while (!done) {
      const { value, done: readerDone } = await reader.read();
      done = readerDone;
      if (value) {
        buffer += decoder.decode(value, { stream: true });
      }

      let newlineIndex = buffer.indexOf('\n');
      while (newlineIndex !== -1) {
        const line = buffer.slice(0, newlineIndex);
        buffer = buffer.slice(newlineIndex + 1);
        if (handleLine(line)) {
          done = true;
          break;
        }
        newlineIndex = buffer.indexOf('\n');
      }
    }

    // Flush any final line that arrived without a trailing newline.
    if (buffer.length > 0) {
      buffer += decoder.decode();
      if (buffer.trim().length > 0) {
        handleLine(buffer);
      }
    }
  }, []);

  // Patch the LabCard message that currently owns the active lab.
  const patchActiveLabCard = useCallback((lab: any) => {
    setMessages((prev) => {
      const next = [...prev];
      for (let i = next.length - 1; i >= 0; i--) {
        if (next[i].metadata?.lab?.active) {
          next[i] = {
            ...next[i],
            metadata: {
              ...next[i].metadata,
              lab: { ...next[i].metadata.lab, ...lab },
            },
          };
          break;
        }
      }
      return next;
    });
  }, []);

  // A hint reveal must render inside the LabCard, not as chat messages: drop
  // the trailing user "hint" + assistant hint bubbles and fold the new hint
  // data into the active lab card.
  const absorbLabHint = useCallback((lab: any) => {
    setMessages((prev) => {
      const next = [...prev];
      if (next.length && next[next.length - 1].role === 'assistant') {
        next.pop();
      }
      if (next.length && next[next.length - 1].role === 'user') {
        next.pop();
      }
      for (let i = next.length - 1; i >= 0; i--) {
        if (next[i].metadata?.lab?.active) {
          next[i] = {
            ...next[i],
            metadata: {
              ...next[i].metadata,
              lab: { ...next[i].metadata.lab, ...lab },
            },
          };
          break;
        }
      }
      return next;
    });
  }, []);

  const sendMessage = useCallback(async (
    text: string,
    attachments?: Array<{ name: string; type: string; content: string }>,
    overrideConversationId?: string,
    labContext?: { action: 'start' | 'resume' | 'answer'; lab_id?: string },
    pageContext?: PageContextPayload,
  ) => {
    if (!text.trim() && (!attachments || attachments.length === 0)) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: text,
      metadata: { attachments: attachments || [] }
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);
    setErrorDetail(null);

    // Placeholder for assistant response
    setMessages((prev) => [...prev, { role: 'assistant', content: '' }]);

    const images: string[] = [];
    const files: Array<{ name: string; type: string; content: string }> = [];

    if (attachments) {
      attachments.forEach((att) => {
        if (att.type.startsWith('image/')) {
          images.push(att.content); // Base64 DataURL
        } else {
          files.push(att); // Text file description/content
        }
      });
    }

    const convId = overrideConversationId || conversationIdRef.current || safeRandomUUID();
    if (!conversationIdRef.current && !overrideConversationId) {
      setConversationId(convId);
      onNewConversation?.(convId);
    }

    const payload: any = {
      query: text || "Analyze attached file/image",
      stream: true,
      conversation_id: convId,
    };

    if (images.length > 0) payload.images = images;
    if (files.length > 0) payload.files = files;
    if (labContext) payload.context = { ...payload.context, lab: labContext };
    if (pageContext) payload.context = { ...payload.context, page: pageContext };
    // Explicit language override is sent ONLY when the user actively picked it
    // this session. An auto-loaded remembered preference is intentionally left
    // out — the backend applies its stored preference + auto-detection override
    // there, so romanized queries still switch languages correctly.
    if (languageToggledRef.current && languageRef.current && languageRef.current !== 'auto') {
      payload.language = languageRef.current;
    }
    // Guests (no JWT) are tracked by a persistent device id so they share the
    // daily free allowance.
    if (!localStorage.getItem("accessToken")) {
      payload.client_id = getGuestId();
    }

    try {
      await streamChat(payload, ({ token, metadata }) => {
        // A lab hint reveal is absorbed into the LabCard (no chat messages).
        if (metadata && metadata.lab?.hint_revealed) {
          absorbLabHint(metadata.lab);
          return;
        }
        setMessages((prev) => {
          const newMessages = [...prev];
          const lastMsg = newMessages[newMessages.length - 1];

          if (token) {
            // Fix table row concatenation during streaming (issue: "| Details ||---|---|| What |" collapsed)
            // Two failure modes:
            // 1) Intra-token: safety-valve flush (512 chars) yields single token with "||---|---|" inside (no \n)
            // 2) Inter-token: "| Details |" + "|---|---|" streamed as separate SSE tokens without \n
            // We normalize both the incoming token and the boundary.
            const normalizeTableChunk = (s: string): string => {
              let out = s;
              // Table fixes (only when "|" present)
              if (out.includes("|")) {
                // Generic row boundary: "alerts || Indexer" or "alerts | | Indexer" -> "alerts |\n| Indexer"
                if (out.includes("---") || out.includes("||") || out.includes("| |")) {
                  out = out.replace(/\|\s*\|\s*/g, "|\n|");
                }
                // Missing newline before separator row when previous text has no \n: "Details | |---|---|"
                out = out.replace(/([^\n])\s+(\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|)/g, (m, p1, p2) => {
                  if (p2.includes("---")) return p1 + "\n" + p2.trimStart();
                  return m;
                });
                // Separator row directly glued to next data row: "|---|---| | **What** |" -> "|---|---| \n| **What** |"
                out = out.replace(/(\|[-:\s|]+\|)\s+(\|)/g, (m, a, b) => (a.includes("---") ? a + "\n" + b : m));
              }
              // Bullet list fixes: "here are 5 key points:- Collection" or "entry point.- Parsing" -> need newline before "- "
              // Handles both intra-token collapsed bullets and inter-token boundaries
              if (out.includes("- ")) {
                // " : - " or ".- " collapsed inside single token: "analyst:- Collection" / "point.- Parsing"
                out = out.replace(/([^\n])\s*:\s*-\s+(?=[A-Z*])/g, "$1:\n- ");
                out = out.replace(/([^\n])\s*\.\s*-\s+(?=[A-Z*])/g, "$1.\n- ");
                // Generic bullet-to-bullet without newline: "point.- Parsing" already handled, also "Ingestion – ...- Parsing"
                // More general: any " - " that is bullet start after previous bullet's text, ensure newline
                // Only when out looks like a list (contains at least two "- " bullets)
                const bulletCount = (out.match(/(^|\n)\s*-\s+/g) || []).length + (out.match(/[^\n]\s*-\s+(?=[A-Z*])/g) || []).length;
                if (bulletCount >= 1 || out.trimStart().startsWith("- ")) {
                  // Fix "entry point.- Parsing" that may have been missed due to en-dash "–"
                  out = out.replace(/([^\n\u2013])\s*-\s+(?=\*\*|[A-Z])/g, (m, p1) => {
                    // Avoid breaking " - " inside "single pane of glass: search" (not bullet)
                    // Only when preceding char is . : or | or already bullet context
                    return m;
                  });
                }
              }
              return out;
            };
            let toAppend = normalizeTableChunk(token);
            const prev = lastMsg.content;
            if (prev && toAppend) {
              const prevTrimEnd = prev.trimEnd();
              const tokenTrimStart = toAppend.trimStart();
              const prevEndsPipe = prevTrimEnd.endsWith("|");
              const prevEndsSep = prevTrimEnd.endsWith("---");
              const nextStartsPipe = tokenTrimStart.startsWith("|");
              const nextStartsSep = /^\|\s*:?-{3,}/.test(tokenTrimStart);
              if (nextStartsPipe) {
                // Table row boundary: pipe -> pipe needs single newline
                if ((prevEndsPipe || prevEndsSep) && nextStartsPipe) {
                  if (!prev.endsWith("\n")) {
                    toAppend = "\n" + toAppend.trimStart();
                  }
                } else if (nextStartsSep) {
                  // separator row starting fresh
                  if (!prev.endsWith("\n")) {
                    toAppend = "\n" + toAppend.trimStart();
                  }
                } else {
                  // Paragraph text -> table header (e.g. "you asked for." + "| Aspect |")
                  // Markdown tables require a blank line before the header. History works
                  // because persisted join adds it, but streaming tokens arrive without.
                  if (!prev.endsWith("\n")) {
                    toAppend = "\n\n" + toAppend.trimStart();
                  } else if (!prev.endsWith("\n\n")) {
                    // prev ends with single \n (e.g. intro "Great question!\n") - ensure blank line
                    toAppend = "\n" + toAppend.trimStart();
                  }
                }
              } else if (nextStartsSep) {
                if (!prev.endsWith("\n")) {
                  toAppend = "\n" + toAppend.trimStart();
                }
              } else if (/^(- |\* |• |\d+\. )/.test(tokenTrimStart)) {
                // Bullet list: "- Collection..." after "here are 5 key points:" or after previous bullet
                // Markdown lists require newline before "- " (and blank line after paragraph)
                // Handles "here are 5 key points:- Collection" -> "here are 5 key points:\n\n- Collection"
                // and "entry point.- Parsing" already fixed intra-token, but also inter-token "- " + "- "
                if (!prev.endsWith("\n")) {
                  // First bullet after paragraph needs blank line
                  if (prevTrimEnd.endsWith(":") || prevTrimEnd.endsWith(".")) {
                    toAppend = "\n\n" + tokenTrimStart;
                  } else {
                    toAppend = "\n" + tokenTrimStart;
                  }
                }
              } else if (prev.includes("\n- ") && toAppend.trim().length > 0 && !toAppend.includes("|")) {
                // Previous was bullet list, next is paragraph/heading after list (e.g., last bullet "Investigation Pivot" + "**Real-world example:**")
                // Without blank line, paragraph is swallowed into last bullet (as seen in image: "tools.Real-world example:")
                // Detect list -> non-list transition: prev had bullets, next is not bullet/table
                const nextIsListContinuation = /^(- |\* |• |\d+\. )/.test(tokenTrimStart) || tokenTrimStart.startsWith("|");
                if (!nextIsListContinuation) {
                  // Next is paragraph like "**Real-world example:**", "From a SOC...", "### Continue", "This topic..."
                  if (!prev.endsWith("\n")) {
                    toAppend = "\n\n" + toAppend.trimStart();
                  } else if (!prev.endsWith("\n\n")) {
                    toAppend = "\n" + toAppend.trimStart();
                  }
                }
              } else if (prevEndsPipe && toAppend.trim().length > 0) {
                // Table row -> paragraph (e.g. "| ... |" + "**Real-world example:**")
                // Needs blank line to close table, otherwise paragraph is swallowed into last cell
                // BUT if toAppend still contains "|" it's a continuation of the same row's cells
                // (e.g. "| Central Server |" + " Aggregates... | Runs... |") -> do NOT add newline
                const isCellContinuation = toAppend.includes("|");
                if (!isCellContinuation) {
                  if (!prev.endsWith("\n")) {
                    toAppend = "\n\n" + toAppend.trimStart();
                  } else if (!prev.endsWith("\n\n")) {
                    toAppend = "\n" + toAppend.trimStart();
                  }
                }
                // else: cell continuation like " Aggregates... |" -> append directly to same row
              } else if (prev && !prev.endsWith("\n") && /^(- |\* |• |\d+\. )/.test(toAppend.trimStart()) && toAppend.trimStart().startsWith("-")) {
                // Fallback bullet handling for tokens that were normalized but still bullet-like
                toAppend = "\n" + toAppend.trimStart();
              }
            }
            // Final safety: if concatenation still left a collapsed table, fix the whole message once
            const combined = prev + toAppend;
            if (combined.includes("||") || combined.includes("|---|")) {
              lastMsg.content = normalizeTableChunk(combined)
                // collapse accidental triple newlines from double-fix
                .replace(/\n{3,}/g, "\n\n");
            } else {
              lastMsg.content = combined;
            }
          }

          // Inject metadata if it arrives
          if (metadata) {
            lastMsg.metadata = { ...lastMsg.metadata, ...metadata };
          }
          return newMessages;
        });
      });
    } catch (err: any) {
      if (err.name === 'AbortError') {
        console.log("Request aborted");
      } else {
        setError(err.message || 'An error occurred during chat');
        setErrorDetail(err as ChatError);
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  }, []);

  // Send a lab hint without creating any chat messages: the response is
  // folded straight into the active LabCard.
  const sendLabHint = useCallback(async () => {
    const convId = conversationIdRef.current || safeRandomUUID();
    if (!conversationIdRef.current) {
      setConversationId(convId);
      onNewConversation?.(convId);
    }
    setIsLoading(true);
    setError(null);

    const payload: any = {
      query: 'hint',
      stream: true,
      conversation_id: convId,
    };
    if (!localStorage.getItem("accessToken")) {
      payload.client_id = getGuestId();
    }
    if (languageRef.current && languageRef.current !== 'auto') {
      payload.language = languageRef.current;
    }

    try {
      await streamChat(payload, ({ metadata }) => {
        if (metadata && metadata.lab) {
          patchActiveLabCard(metadata.lab);
        }
      });
    } catch (err: any) {
      if (err.name !== 'AbortError') {
        setError(err.message || 'An error occurred during chat');
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  }, []);

  const stopGenerating = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsLoading(false);
    }
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
    setErrorDetail(null);
    try {
      sessionStorage.removeItem(SESSION_STORAGE_KEY);
      sessionStorage.removeItem(CONVERSATION_ID_STORAGE_KEY);
    } catch {
      // best-effort
    }
    lastPublishedHashRef.current = null;
    try {
      channelRef.current?.postMessage({
        type: 'clear',
        instanceId: instanceIdRef.current,
        conversationId: null,
      });
    } catch {
      // best-effort
    }
  }, []);

  const startNewConversation = useCallback(() => {
    const newId = safeRandomUUID();
    setConversationId(newId);
    setMessages([]);
    setError(null);
    setErrorDetail(null);
    try {
      sessionStorage.removeItem(SESSION_STORAGE_KEY);
      // Always clear the stored conversation id for New Chat — otherwise a
      // stale id could be resumed (and messages re-grouped into the old
      // thread) after a page reload.
      sessionStorage.removeItem(CONVERSATION_ID_STORAGE_KEY);
      sessionStorage.setItem(
        `bt_chat_conversation_${newId}_restoring`,
        'true'
      );
    } catch {
      // best-effort
    }
    lastPublishedHashRef.current = null;
    try {
      channelRef.current?.postMessage({
        type: 'clear',
        instanceId: instanceIdRef.current,
        conversationId: newId,
      });
    } catch {
      // best-effort
    }
    onNewConversation?.(newId);
  }, [onNewConversation]);

  const loadConversation = useCallback(async (id: string) => {
    setConversationId(id);
    setError(null);
    setErrorDetail(null);
    setIsLoading(true);
    try {
      const accessToken = localStorage.getItem('accessToken');
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      if (accessToken) headers['Authorization'] = `Bearer ${accessToken}`;

      const response = await fetch(apiUrl(`/api/conversations/${id}`), {
        method: 'GET',
        headers,
      });
      if (!response.ok) throw new Error(`Error: ${response.status} ${response.statusText}`);
      const convo = await response.json();
      const loaded: ChatMessage[] = (convo.messages || []).map((m: any) => ({
        role: m.role as 'user' | 'assistant',
        content: m.content,
        metadata: m.metadata || {},
      }));
      setMessages(loaded);
      try {
        sessionStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(loaded));
      } catch {}
    } catch (err: any) {
      console.error('Failed to load conversation:', err);
      setError(err.message || 'Failed to load conversation');
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Default welcome shown instantly when the workspace opens, before (or instead
  // of) the server-generated greeting. Uses the signed-in user's name so a new
  // chat never opens blank even if the platform session fetch is slow or down.
  const buildDefaultWelcome = useCallback((): ChatMessage => {
    let name = "";
    try {
      name = localStorage.getItem("userFullName") || "";
      if (!name) {
        name = (localStorage.getItem("userEmail") || "").split("@")[0] || "";
      }
    } catch {
      // storage unavailable -> anonymous greeting
    }
    const greeting = name ? `Hey ${name}!` : "Hey there!";
    return {
      role: "assistant",
      content:
        `${greeting} Welcome to BlueTeamers AI — your SOC mentor for cybersecurity. ` +
        "I can explain security concepts (MITRE ATT&CK, SIEM, log analysis), help you " +
        "analyze logs and alerts, quiz you on your courses, or guide you through practice labs. " +
        "What would you like to work on today?",
    };
  }, []);

  const initializeSession = useCallback(async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) return;

    // A BroadcastChannel sync may have already applied the live conversation
    // (floating window -> newly-opened workspace tab). Never overwrite it with
    // a fresh greeting; guard the in-flight fetch below the same way.
    //
    // Use the render-time `messages` here, NOT messagesRef: this callback is
    // recreated whenever messages.length changes, so after "New Chat" clears
    // the thread the Chat effect re-runs this with an EMPTY snapshot, while
    // messagesRef may still hold the previous conversation (its sync effect
    // lives in the provider and runs after this child's effect). Reading the
    // stale ref made New Chat skip seeding the welcome until a page refresh.
    if (messages.length > 0) return;

    // Restore a previous in-app conversation (e.g. returning from a course
    // page via Browser Back) instead of starting a fresh session.
    if (messages.length === 0) {
      try {
        const saved = sessionStorage.getItem(SESSION_STORAGE_KEY);
        if (saved) {
          const parsed = JSON.parse(saved);
          // Only restore an actual in-progress conversation (one that contains a
          // user message, e.g. when returning from a course via Browser Back). A
          // lone welcome/dashboard init message should be re-fetched fresh so the
          // dashboard always reflects current user data instead of stale cache.
          if (Array.isArray(parsed) && parsed.some(m => m && m.role === 'user')) {
            setMessages(parsed);
            // Resume the same conversation id so the floating assistant and the
            // /chat workspace keep continuing the same thread.
            const savedId = sessionStorage.getItem(CONVERSATION_ID_STORAGE_KEY);
            if (savedId && !conversationIdRef.current) {
              setConversationId(savedId);
            }
            return;
          }
        }
      } catch {
        // Corrupt/unavailable storage -> fall through to a fresh session.
      }
    }

    if (messages.length > 0) return;

    // Show a name-aware welcome instantly so the workspace never opens blank.
    // The server greeting (fetched below) replaces it when the platform session
    // loads successfully; if that call fails, this default welcome stays.
    setMessages([buildDefaultWelcome()]);

    try {
      setIsLoading(true);
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      };

      const response = await fetch(apiUrl('/api/chat/session'), {
        method: 'GET',
        headers,
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      // A sync landed while the greeting fetch was in flight — keep the live
      // conversation and drop the greeting.
      if (messagesRef.current.length > 0) return;

      const welcomeMsg: ChatMessage = {
        role: 'assistant',
        content: data.welcome_message,
        metadata: {
          platform: {
             context: data.platform_context
          }
        }
      };

      setMessages([welcomeMsg]);
    } catch (err: any) {
      console.error("Failed to initialize session:", err);
    } finally {
      setIsLoading(false);
    }
  }, [messages.length, buildDefaultWelcome]);

  // Sync the floating assistant to the latest conversation persisted by the
  // /chat workspace. Unlike initializeSession (which only restores when THIS
  // instance is empty), it always re-reads sessionStorage so reopening the
  // floating window reflects the full-screen conversation even though this
  // instance already holds older in-memory messages. Falls back to the normal
  // session init when there is nothing meaningful saved.
  const syncFromSession = useCallback(async () => {
    try {
      const saved = sessionStorage.getItem(SESSION_STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.some((m: ChatMessage) => m && m.role === 'user')) {
          setMessages(parsed);
          const savedId = sessionStorage.getItem(CONVERSATION_ID_STORAGE_KEY);
          if (savedId) {
            setConversationId(savedId);
          }
          return;
        }
      }
    } catch {
      // Corrupt/unavailable storage -> fall through to a fresh session.
    }
    await initializeSession();
  }, [initializeSession]);

  return {
    messages,
    sendMessage,
    sendLabHint,
    isLoading,
    error,
    errorDetail,
    stopGenerating,
    clearMessages,
    startNewConversation,
    loadConversation,
    initializeSession,
    syncFromSession,
    conversationId,
    language,
    setLanguage,
  };
}
