import { useState, useRef, useCallback, useEffect } from 'react';
import { apiUrl } from '../services/api';
import type { PageContextPayload } from '../lib/pageContext';
import { getGuestId } from '../lib/guestId';

const SESSION_STORAGE_KEY = 'bt_chat_messages_v1';
const CONVERSATION_ID_STORAGE_KEY = 'bt_chat_conversation_id_v1';
const LANGUAGE_STORAGE_KEY = 'bt_chat_language_v1';

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

    const convId = overrideConversationId || conversationIdRef.current || crypto.randomUUID();
    if (!conversationIdRef.current && !overrideConversationId) {
      setConversationId(convId);
      onNewConversation?.(convId);
    }

    const payload: any = {
      query: text || "Analyze attached file/image",
      stream: true,
      conversation_id: convId,
      user_id: "demo_user",
      token: localStorage.getItem("accessToken") || undefined,
    };

    if (images.length > 0) payload.images = images;
    if (files.length > 0) payload.files = files;
    if (labContext) payload.context = { ...payload.context, lab: labContext };
    if (pageContext) payload.context = { ...payload.context, page: pageContext };
    // Manual language preference (Auto Detect is omitted -> backend detects).
    if (languageRef.current && languageRef.current !== 'auto') {
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
            lastMsg.content += token;
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
    const convId = conversationIdRef.current || crypto.randomUUID();
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
      user_id: 'demo_user',
      token: localStorage.getItem("accessToken") || undefined,
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
  }, []);

  const startNewConversation = useCallback(() => {
    const newId = crypto.randomUUID();
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

  const initializeSession = useCallback(async () => {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) return;

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
  }, [messages.length]);

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
    conversationId,
    language,
    setLanguage,
  };
}
