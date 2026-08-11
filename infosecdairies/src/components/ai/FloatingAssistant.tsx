/**
 * FloatingAssistant — the global floating AI assistant.
 *
 * A launcher button (bottom-right) with a free-message badge opens a compact chat
 * window on every authenticated page except /chat (which has the full workspace).
 * The window shares the same `useChat` session storage as the workspace, so the
 * conversation continues seamlessly between the two surfaces.
 */

import React, { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { ChatMarkdown } from "@/components/ui/chat/ChatMarkdown";
import {
  Brain,
  X,
  Minimize2,
  Maximize2,
  ExternalLink,
  Crown,
  Sparkles,
  User,
} from "lucide-react";
import logo from "@/assets/logo-color.png";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ChatInput } from "@/components/ui/chat/ChatInput";
import { UpgradeDialog } from "@/components/ai/UpgradeDialog";
import { useAiAssistant } from "@/context/AiAssistantContext";
import { useAuth } from "@/context/AuthContext";
import { cn } from "@/lib/utils";

const FREE_LIMIT = 5;

const BUTTON_SIZE = 56;
const MARGIN = 16;
const DRAG_THRESHOLD = 5;
const LAUNCHER_POS_KEY = "bt-ai-launcher-pos";
const WIN_POS_KEY = "bt-ai-window-pos";

const clamp = (v: number, min: number, max: number) => Math.max(min, Math.min(max, v));

const getDefaultLauncherPos = () => ({
  x: window.innerWidth - BUTTON_SIZE - MARGIN,
  y: window.innerHeight - BUTTON_SIZE - MARGIN,
});

const getSavedLauncherPos = () => {
  try {
    const saved = localStorage.getItem(LAUNCHER_POS_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      if (typeof parsed?.x === "number" && typeof parsed?.y === "number") {
        // Clamp immediately to the current viewport so a stale or off-screen
        // saved position never hides the launcher after a reload.
        const maxX = Math.max(MARGIN, window.innerWidth - BUTTON_SIZE - MARGIN);
        const maxY = Math.max(MARGIN, window.innerHeight - BUTTON_SIZE - MARGIN);
        return {
          x: clamp(parsed.x, MARGIN, maxX),
          y: clamp(parsed.y, MARGIN, maxY),
        };
      }
    }
  } catch {
    /* ignore malformed saved position */
  }
  return null;
};

const getSavedWinPos = () => {
  try {
    const saved = localStorage.getItem(WIN_POS_KEY);
    if (saved) {
      const parsed = JSON.parse(saved);
      if (typeof parsed?.x === "number" && typeof parsed?.y === "number") {
        return { x: parsed.x, y: parsed.y };
      }
    }
  } catch {
    /* ignore malformed saved position */
  }
  return null;
};

export const FloatingAssistant: React.FC = () => {
  const {
    isOpen,
    isMinimized,
    close,
    minimize,
    expand,
    open,
    pageContext,
    access,
    chatState,
  } = useAiAssistant();
  const { isAuthenticated } = useAuth();
  const { messages, sendMessage, isLoading, stopGenerating, initializeSession, error, language, setLanguage } = chatState;

  const location = useLocation();
  const navigate = useNavigate();
  const scrollRef = useRef<HTMLDivElement>(null);
  const isGuest = !isAuthenticated;

  // Draggable launcher position (persisted so it survives page navigation).
  const [pos, setPos] = useState(() => getSavedLauncherPos() ?? getDefaultLauncherPos());
  const [dragging, setDragging] = useState(false);
  const dragRef = useRef<{
    startX: number;
    startY: number;
    originX: number;
    originY: number;
    moved: boolean;
  } | null>(null);
  const suppressClickRef = useRef(false);

  // Draggable window position (null = anchored to the launcher).
  const [winPos, setWinPos] = useState<{ x: number; y: number } | null>(getSavedWinPos);
  const [windowDragging, setWindowDragging] = useState(false);
  const windowDragRef = useRef<{
    startX: number;
    startY: number;
    originX: number;
    originY: number;
  } | null>(null);

  useEffect(() => {
    try {
      if (winPos) {
        localStorage.setItem(WIN_POS_KEY, JSON.stringify(winPos));
      }
    } catch {
      /* ignore storage errors */
    }
  }, [winPos]);

  useEffect(() => {
    try {
      localStorage.setItem(LAUNCHER_POS_KEY, JSON.stringify(pos));
    } catch {
      /* ignore storage errors */
    }
  }, [pos]);

  // Keep the launcher inside the viewport if the window resizes.
  useEffect(() => {
    const onResize = () => {
      const maxX = Math.max(MARGIN, window.innerWidth - BUTTON_SIZE - MARGIN);
      const maxY = Math.max(MARGIN, window.innerHeight - BUTTON_SIZE - MARGIN);
      setPos((p) => ({
        x: clamp(p.x, MARGIN, maxX),
        y: clamp(p.y, MARGIN, maxY),
      }));
      setWinPos((p) => {
        if (!p) return p;
        const winW = Math.min(window.innerWidth * 0.92, 380);
        const winH = Math.min(window.innerHeight * 0.68, 560);
        return {
          x: clamp(p.x, 8, Math.max(8, window.innerWidth - winW - 8)),
          y: clamp(p.y, 8, Math.max(8, window.innerHeight - winH - 8)),
        };
      });
    };
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  const onLauncherPointerDown = (e: React.PointerEvent<HTMLButtonElement>) => {
    if (!e.isPrimary) return;
    e.preventDefault();
    dragRef.current = {
      startX: e.clientX,
      startY: e.clientY,
      originX: pos.x,
      originY: pos.y,
      moved: false,
    };
    setDragging(true);
    e.currentTarget.setPointerCapture(e.pointerId);
  };

  const onLauncherPointerMove = (e: React.PointerEvent<HTMLButtonElement>) => {
    const drag = dragRef.current;
    if (!drag) return;
    const dx = e.clientX - drag.startX;
    const dy = e.clientY - drag.startY;
    if (!drag.moved && Math.hypot(dx, dy) > DRAG_THRESHOLD) {
      drag.moved = true;
    }
    if (drag.moved) {
      const maxX = Math.max(MARGIN, window.innerWidth - BUTTON_SIZE - MARGIN);
      const maxY = Math.max(MARGIN, window.innerHeight - BUTTON_SIZE - MARGIN);
      setPos({
        x: clamp(drag.originX + dx, MARGIN, maxX),
        y: clamp(drag.originY + dy, MARGIN, maxY),
      });
    }
  };

  const onLauncherPointerUp = () => {
    const drag = dragRef.current;
    dragRef.current = null;
    setDragging(false);
    if (drag?.moved) {
      suppressClickRef.current = true;
    }
  };

  const onLauncherClick = () => {
    if (suppressClickRef.current) {
      suppressClickRef.current = false;
      return;
    }
    open();
  };

  const onWindowPointerDown = (e: React.PointerEvent<HTMLDivElement>) => {
    if (!e.isPrimary) return;
    e.preventDefault();
    windowDragRef.current = {
      startX: e.clientX,
      startY: e.clientY,
      originX: renderedWinX,
      originY: renderedWinY,
    };
    setWindowDragging(true);
    e.currentTarget.setPointerCapture(e.pointerId);
  };

  const onWindowPointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
    const d = windowDragRef.current;
    if (!d) return;
    const maxX = Math.max(8, window.innerWidth - winW - 8);
    const maxY = Math.max(8, window.innerHeight - winH - 8);
    setWinPos({
      x: clamp(d.originX + (e.clientX - d.startX), 8, maxX),
      y: clamp(d.originY + (e.clientY - d.startY), 8, maxY),
    });
  };

  const onWindowPointerUp = () => {
    windowDragRef.current = null;
    setWindowDragging(false);
  };

  // Position the chat window / minimized pill relative to the launcher.
  const winW = Math.min(window.innerWidth * 0.92, 380);
  const winH = Math.min(window.innerHeight * 0.68, 560);
  const anchorWinX = clamp(
    pos.x + BUTTON_SIZE / 2 - winW / 2,
    8,
    Math.max(8, window.innerWidth - winW - 8),
  );
  const anchorWinY =
    pos.y - winH - 12 >= 8
      ? pos.y - winH - 12
      : clamp(pos.y + BUTTON_SIZE + 12, 8, Math.max(8, window.innerHeight - winH - 8));
  const renderedWinX = clamp(
    winPos?.x ?? anchorWinX,
    8,
    Math.max(8, window.innerWidth - winW - 8),
  );
  const renderedWinY = clamp(
    winPos?.y ?? anchorWinY,
    8,
    Math.max(8, window.innerHeight - winH - 8),
  );
  const pillX = clamp(
    renderedWinX + winW - 300,
    8,
    Math.max(8, window.innerWidth - 300 - 8),
  );
  const pillY =
    renderedWinY - 76 >= 8
      ? renderedWinY - 76
      : clamp(renderedWinY + winH + 12, 8, window.innerHeight - 48);

  // The full workspace lives at /chat — don't double up the floating window there.
  useEffect(() => {
    if (location.pathname === "/chat" && isOpen) {
      close();
    }
  }, [location.pathname, isOpen, close]);

  // Initialize/restore the shared conversation when the window first opens.
  useEffect(() => {
    if (isOpen) {
      initializeSession();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen]);

  // Keep the message list scrolled to the latest message.
  useEffect(() => {
    const viewport = scrollRef.current?.querySelector("[data-radix-scroll-area-viewport]");
    if (viewport) {
      (viewport as HTMLElement).scrollTop = (viewport as HTMLElement).scrollHeight;
    }
  }, [messages, isLoading]);

  const isFree = access?.access_level === "free";
  const remaining = isFree ? access?.remaining : undefined;
  const limit = isFree ? (access?.limit ?? FREE_LIMIT) : 0;
  const used = isFree ? (access?.used ?? 0) : 0;

  // Availability state for the launcher's status ember.
  const ember =
    isFree && remaining === 0
      ? "bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.8)]"
      : isFree && remaining === 1
      ? "bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.8)]"
      : "bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]";

  const handleSend = (text: string) => {
    sendMessage(text, undefined, undefined, undefined, pageContext);
  };

  // The backend streams into an empty assistant placeholder message while
  // `isLoading` is true. Hide that empty bubble and show the typing indicator
  // instead, so only one logo is visible while a response is loading.
  const lastMsg = messages[messages.length - 1];
  const isStreamingAssistant = Boolean(
    isLoading && lastMsg?.role === "assistant" && !lastMsg.content,
  );
  const showTypingIndicator =
    isLoading && (isStreamingAssistant || !lastMsg || lastMsg.role !== "assistant");

  const pageLabel = pageContext?.lesson_title
    ? pageContext.lesson_title
    : pageContext?.lab_title
    ? pageContext.lab_title
    : pageContext?.course_title
    ? pageContext.course_title
    : undefined;

  if (!isOpen) {
    return (
      <>
        <button
          onPointerDown={onLauncherPointerDown}
          onPointerMove={onLauncherPointerMove}
          onPointerUp={onLauncherPointerUp}
          onClick={onLauncherClick}
          aria-label="Open BlueTeamers AI"
          style={{ left: pos.x, top: pos.y, touchAction: "none" }}
          className={cn(
            "group fixed z-50 h-14 w-14 overflow-hidden rounded-2xl border border-zinc-600/70 bg-[#05272e] shadow-[0_10px_30px_rgba(0,0,0,0.5)] ring-1 ring-inset ring-white/10",
            dragging
              ? "cursor-grabbing transition-none"
              : "transition-all hover:scale-105 hover:border-primary/40 hover:shadow-[0_10px_40px_rgba(6,141,164,0.35)]",
          )}
        >
          <img
            src={logo}
            alt=""
            className="h-full w-full object-cover"
            draggable={false}
          />
          {/* Status ember: green = messages left, amber = last one, red = done */}
          <span
            className={cn(
              "absolute bottom-1 right-1 h-3 w-3 rounded-full border-2 border-black/80 transition-all",
              ember,
            )}
          />
        </button>
        <UpgradeDialog variant="limit" />
      </>
    );
  }

  // Minimized: a compact pill bar above the launcher position.
  if (isMinimized) {
    return (
      <>
        <div
          style={{ left: pillX, top: pillY }}
          className="fixed z-50 flex w-[300px] max-w-[calc(100vw-2.5rem)] items-center gap-2 rounded-xl border border-border bg-background/95 p-2 shadow-2xl backdrop-blur"
        >
          <button
            onClick={expand}
            className="flex min-w-0 flex-1 items-center gap-2 rounded-lg px-2 py-1.5 text-left hover:bg-muted transition-colors"
          >
            <div className="flex h-7 w-7 shrink-0 items-center justify-center overflow-hidden rounded-lg border border-primary/30 bg-[#05272e]">
              <img src={logo} alt="" className="h-full w-full object-cover" />
            </div>
            <div className="min-w-0">
              <div className="truncate text-xs font-medium text-foreground">BlueTeamers AI</div>
              {pageLabel && (
                <div className="truncate text-[10px] text-muted-foreground">{pageLabel}</div>
              )}
            </div>
          </button>
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={expand} aria-label="Expand">
            <Maximize2 className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" className="h-8 w-8" onClick={close} aria-label="Close">
            <X className="h-4 w-4" />
          </Button>
        </div>
        <UpgradeDialog variant="limit" />
      </>
    );
  }

  return (
    <>
      <div
        style={{ left: renderedWinX, top: renderedWinY, width: winW, height: winH }}
        className="fixed z-50 flex flex-col overflow-hidden rounded-2xl border border-primary/20 bg-background/95 shadow-2xl backdrop-blur-xl animate-in fade-in"
      >
        {/* Header (draggable) */}
        <div
          onPointerDown={onWindowPointerDown}
          onPointerMove={onWindowPointerMove}
          onPointerUp={onWindowPointerUp}
          className={cn(
            "flex items-center gap-2 border-b border-border/60 bg-gradient-to-r from-primary/10 via-transparent to-transparent px-3 py-2.5",
            windowDragging ? "cursor-grabbing" : "cursor-grab",
          )}
          style={{ touchAction: "none" }}
        >
          <div className="flex h-8 w-8 shrink-0 items-center justify-center overflow-hidden rounded-lg border border-primary/30 bg-[#05272e]">
            <img src={logo} alt="BlueTeamers" className="h-full w-full object-cover" />
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-1.5 text-sm font-semibold text-foreground">
              BlueTeamers AI
              {isFree && (
                <span className="text-[9px] font-mono text-primary">
                  {isGuest ? "GUEST · FREE" : "FREE"}
                </span>
              )}
            </div>
            {pageLabel && (
              <div className="flex items-center gap-1 truncate text-[10px] text-muted-foreground">
                <Sparkles className="h-2.5 w-2.5 shrink-0 text-primary" />
                <span className="truncate">On: {pageLabel}</span>
              </div>
            )}
          </div>
          <div className="flex shrink-0 items-center gap-0.5" onPointerDown={(e) => e.stopPropagation()}>
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7"
              onClick={() => navigate("/chat")}
              title="Open in full workspace"
            >
              <ExternalLink className="h-3.5 w-3.5" />
            </Button>
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={minimize} title="Minimize">
              <Minimize2 className="h-3.5 w-3.5" />
            </Button>
            <Button variant="ghost" size="icon" className="h-7 w-7" onClick={close} title="Close">
              <X className="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>

        {/* Messages */}
        <ScrollArea className="flex-1" ref={scrollRef}>
          <div className="flex flex-col gap-3 px-3 py-3">
            {messages.length === 0 && !isLoading && (
              <div className="mx-auto mt-6 max-w-[240px] text-center">
                <div className="mx-auto mb-2 flex h-10 w-10 items-center justify-center rounded-xl border border-primary/30 bg-primary/10">
                  <Brain className="h-5 w-5 text-primary" />
                </div>
                <p className="text-xs text-muted-foreground">
                  {isGuest
                    ? "Ask anything about this page — no login needed. Login and join a course for unlimited AI."
                    : "Ask anything about the page you're on, your courses, or BlueTeamers in general."}
                </p>
                {isFree && (
                  <p className="mt-2 text-[10px] font-mono text-primary">
                    {remaining > 0 ? `${remaining} free today` : "out of free messages"}
                  </p>
                )}
              </div>
            )}

            {messages.map((msg, idx) => {
              if (isStreamingAssistant && idx === messages.length - 1) {
                return null;
              }
              return (
                <div
                  key={idx}
                  className={cn(
                    "flex items-start gap-2 animate-in fade-in slide-in-from-bottom-2",
                    msg.role === "user" ? "flex-row-reverse" : "flex-row",
                  )}
                >
                  <div
                    className={cn(
                      "flex h-6 w-6 shrink-0 items-center justify-center rounded-lg border mt-1",
                      msg.role === "user"
                        ? "border-primary/40 bg-primary/20 text-primary"
                        : "border-zinc-700 bg-zinc-900",
                    )}
                  >
                    {msg.role === "user" ? (
                      <User className="h-3.5 w-3.5" />
                    ) : (
                      <img src={logo} alt="BlueTeamers" className="h-full w-full rounded object-contain" />
                    )}
                  </div>
                  <div
                    className={cn(
                      "flex flex-col min-w-0 max-w-[85%]",
                      msg.role === "user" ? "items-end" : "items-start",
                    )}
                  >
                    <div
                      className={cn(
                        "rounded-2xl border prose prose-zinc prose-invert prose-sm max-w-none",
                        msg.role === "user"
                          ? "rounded-tr-sm border-primary/20 bg-primary/10 px-3.5 py-2 text-foreground"
                          : "rounded-tl-sm border-zinc-800 bg-zinc-900/80 backdrop-blur-sm px-3.5 py-2.5 text-zinc-100 shadow-[0_0_15px_rgba(0,0,0,0.2)]",
                      )}
                    >
                      <div
                        className={cn(
                          msg.role === "assistant" ? "bt-cyber-message" : "bt-mono bt-user-prose",
                        )}
                      >
                        <ChatMarkdown isStreaming={idx === messages.length - 1 && isLoading}>
                          {msg.content || ""}
                        </ChatMarkdown>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}

            {showTypingIndicator && (
              <div className="flex items-start gap-2">
                <div className="flex h-6 w-6 items-center justify-center rounded-lg border border-zinc-700 bg-zinc-900">
                  <img src={logo} alt="" className="h-full w-full rounded object-contain" />
                </div>
                <div className="flex items-center gap-1.5 rounded-2xl rounded-tl-sm border border-zinc-800 bg-zinc-900/80 px-3.5 py-2.5">
                  <span className="flex gap-1">
                    {[0, 1, 2].map((i) => (
                      <span
                        key={i}
                        className="h-1.5 w-1.5 rounded-full bg-primary animate-dot-pulse"
                        style={{ animationDelay: `${i * 0.2}s` }}
                      />
                    ))}
                  </span>
                </div>
              </div>
            )}

            {error && (
              <div className="rounded-xl border border-destructive/20 bg-destructive/10 p-2.5 text-center font-mono text-[10px] text-destructive">
                {error}
              </div>
            )}
          </div>
        </ScrollArea>

        {/* Free-limit ticket tray: one ticket per free message. Using one
            punches a hole in it; out of tickets means out of free messages. */}
        {isFree && (
          <div className="border-t border-border/60 px-3 py-2">
            <div className="flex items-center justify-center gap-1.5">
              {Array.from({ length: Math.max(1, limit) }).map((_, i) => {
                const spent = i < used;
                return (
                  <span
                    key={i}
                    className={cn(
                      "relative block h-4 w-7 rounded-[4px] border transition-all duration-300",
                      spent
                        ? "border-zinc-700/80 bg-zinc-900/60"
                        : "border-primary/40 bg-primary/10 shadow-[0_0_10px_rgba(0,186,216,0.15)]",
                    )}
                  >
                    {spent ? (
                      <span className="absolute inset-0 flex items-center justify-center">
                        <span className="h-1.5 w-1.5 rounded-full border border-zinc-600 bg-zinc-950" />
                      </span>
                    ) : (
                      <span className="absolute inset-0 flex items-center justify-center">
                        <span className="h-1 w-1 rounded-full bg-primary/80" />
                      </span>
                    )}
                  </span>
                );
              })}
            </div>
            <div className="mt-1.5 flex items-center justify-center text-[10px]">
              {remaining !== undefined && remaining > 0 ? (
                <span className="font-mono text-muted-foreground">
                  <span className="font-semibold text-foreground">{remaining}</span> free today — keep
                  going
                </span>
              ) : (
                <button
                  onClick={() => navigate(isGuest ? "/auth" : "/courses")}
                  className="flex items-center gap-1 font-mono text-primary hover:underline"
                >
                  <Crown className="h-3 w-3" />
                  {isGuest ? "Login for full access" : "Join a course for unlimited"}
                </button>
              )}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="px-2 pb-2">
          <ChatInput
            onSendMessage={handleSend}
            onStop={stopGenerating}
            isLoading={isLoading}
            language={language}
            onLanguageChange={setLanguage}
          />
        </div>
      </div>
      <UpgradeDialog variant="limit" />
    </>
  );
};
