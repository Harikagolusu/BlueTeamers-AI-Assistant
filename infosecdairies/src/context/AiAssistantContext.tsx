/**
 * AiAssistantContext — global state for the floating AI assistant shown on every
 * authenticated page. It owns the open/minimized window state, the detected page
 * context, the freemium access status, and the upgrade dialog. The chat logic
 * itself is the shared `useChat` hook, so the floating window and the /chat
 * workspace continue the same conversation via sessionStorage.
 */

import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { useChat } from "@/hooks/useChat";
import { useAiAccess, type AiAccessStatus } from "@/hooks/useAiAccess";
import { usePageContext } from "@/hooks/usePageContext";
import type { PageContextPayload } from "@/lib/pageContext";

// Lazy-load the floating assistant UI so it doesn't inflate the initial bundle.
const FloatingAssistant = React.lazy(() =>
  import("@/components/ai/FloatingAssistant").then((m) => ({ default: m.FloatingAssistant })),
);

// Pages where the floating assistant is hidden (full workspace / auth pages).
const HIDDEN_PATHS = new Set(["/chat", "/auth", "/login"]);

interface AiAssistantContextValue {
  isOpen: boolean;
  upgradeOpen: boolean;
  pageContext: PageContextPayload;
  access: AiAccessStatus | null;
  chatState: ReturnType<typeof useChat>;
  open: () => void;
  close: () => void;
  openUpgrade: () => void;
  closeUpgrade: () => void;
}

const AiAssistantContext = createContext<AiAssistantContextValue | undefined>(undefined);

export const AiAssistantProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const chatState = useChat();
  const { status: access, refresh: refreshAccess } = useAiAccess();
  const pageContext = usePageContext();

  const [isOpen, setIsOpen] = useState(false);
  const [upgradeOpen, setUpgradeOpen] = useState(false);

  // The floating assistant is available on every page — including for visitors
  // who are not logged in (they get the guest daily allowance). It is only
  // hidden on the /chat workspace and auth pages.
  const showAssistant = !HIDDEN_PATHS.has(location.pathname);

  // When we navigate onto a hidden page (e.g. /chat), reset the window state so
  // it doesn't auto-reopen when we come back.
  useEffect(() => {
    if (HIDDEN_PATHS.has(location.pathname)) {
      setIsOpen(false);
    }
  }, [location.pathname]);

  // Free users hit the daily limit when the backend returns 429
  // free_ai_limit_reached — surface the upgrade dialog in that case.
  useEffect(() => {
    if (chatState.errorDetail?.code === "free_ai_limit_reached") {
      setUpgradeOpen(true);
    }
  }, [chatState.errorDetail]);

  // After every successful send, refresh the remaining free-message count.
  const lastMessageCount = chatState.messages.length;
  useEffect(() => {
    if (lastMessageCount > 0 && access?.access_level === "free" && !chatState.isLoading) {
      refreshAccess();
    }
  }, [lastMessageCount, chatState.isLoading, access?.access_level, refreshAccess]);

  const value = useMemo<AiAssistantContextValue>(
    () => ({
      isOpen,
      upgradeOpen,
      pageContext,
      access,
      chatState,
      open: () => {
        setIsOpen(true);
      },
      close: () => {
        setIsOpen(false);
      },
      openUpgrade: () => setUpgradeOpen(true),
      closeUpgrade: () => setUpgradeOpen(false),
    }),
    [isOpen, upgradeOpen, pageContext, access, chatState],
  );

  return (
    <AiAssistantContext.Provider value={value}>
      {children}
      {showAssistant && (
        <React.Suspense fallback={null}>
          <FloatingAssistant />
        </React.Suspense>
      )}
    </AiAssistantContext.Provider>
  );
};

export const useAiAssistant = (): AiAssistantContextValue => {
  const ctx = useContext(AiAssistantContext);
  if (!ctx) throw new Error("useAiAssistant must be used within an AiAssistantProvider");
  return ctx;
};
