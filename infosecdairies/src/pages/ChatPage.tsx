import React, { useEffect, useRef } from 'react';
import { Helmet } from 'react-helmet-async';
import { useNavigate } from 'react-router-dom';
import { Crown, Sparkles, Shield } from 'lucide-react';
import Navbar from '@/components/Navbar';
import { Chat } from '@/components/ui/Chat';
import { WorkspaceSidebar } from '@/components/ui/chat/WorkspaceSidebar';
import { useChat } from '@/hooks/useChat';
import { useConversations } from '@/hooks/useConversations';
import { useAiAssistant } from '@/context/AiAssistantContext';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';


const ChatPage = () => {
  const [sidebarOpen, setSidebarOpen] = React.useState(false);
  const navigate = useNavigate();

  // Both hooks are called at the top level — every render, every hook runs.
  // This keeps React's rules-of-hooks happy and ensures state updates
  // propagate correctly to ChatPage (and thus to its children).
  const convState = useConversations();
  const chatState = useChat();
  const { conversationId, isLoading } = chatState;

  // Freemium: only guests (not logged in) are kept out of the full workspace —
  // they get their free chats from the floating window. Logged-in users (even
  // without a course purchase) can open the workspace and use their free chats;
  // the backend enforces the message limit / premium upgrades.
  //
  // FAIL-CLOSED: an unknown or errored access status must NOT silently grant a
  // guest full access. Guests are gated unless we positively know they are
  // premium (e.g. the freemium feature is disabled server-side).
  const { access } = useAiAssistant();
  const { isAuthenticated } = useAuth();
  const isGuest = !isAuthenticated;
  const gated = isGuest && access?.is_premium !== true;

  // Track the previous conversation ID so we can detect *new* conversations.
  const prevConvIdRef = useRef<string | null>(null);

  // When a new conversation finishes loading (response received = backend
  // has already persisted the turn), refresh the sidebar list so the new
  // conversation appears in Recent Conversations.
  useEffect(() => {
    if (conversationId && conversationId !== prevConvIdRef.current && !isLoading) {
      convState.refresh();
      prevConvIdRef.current = conversationId;
    }
  }, [conversationId, isLoading, convState]);

  // New conversation: clear messages + generate a new ID.
  const handleNewChat = React.useCallback(() => {
    chatState.startNewConversation();
    convState.refresh();
    setSidebarOpen(false);
  }, [chatState, convState]);

  // Resume an existing conversation: load its history and switch the active id.
  const handleSelectConversation = React.useCallback(async (id: string) => {
    await chatState.loadConversation(id);
    await convState.open(id);
    setSidebarOpen(false);
  }, [chatState, convState]);

  // Close the sidebar when the user presses Escape.
  useEffect(() => {
    if (!sidebarOpen) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setSidebarOpen(false);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [sidebarOpen]);

  // Guests (not logged in) see the sign-in prompt instead of the full workspace —
  // they use their free chats from the floating window. After login the workspace
  // opens and free chats apply until the user purchases a course.
  if (gated) {
    return (
      <div className="h-[100dvh] bg-background flex flex-col overflow-hidden">
        <Helmet>
          <title>AI Workspace | BlueTeamers</title>
        </Helmet>
        <Navbar variant="floating" />
        <main className="flex-1 min-h-0 flex items-center justify-center px-4">
          <div className="w-full max-w-md text-center animate-in fade-in slide-in-from-bottom-4">
            <div className="mx-auto mb-5 inline-flex h-16 w-16 items-center justify-center rounded-2xl border border-primary/30 bg-primary/10 shadow-[0_0_30px_rgba(0,186,216,0.15)]">
              <Crown className="h-8 w-8 text-primary" />
            </div>
            <h1 className="text-2xl font-bold text-foreground">Login to unlock the AI Workspace</h1>
            <p className="mx-auto mt-3 max-w-sm text-sm leading-relaxed text-muted-foreground">
              Sign in to open the full-screen workspace — full page context, file analysis, and practice labs. Guests can chat from the floating window.
            </p>
            <div className="mx-auto mt-6 flex max-w-sm flex-col gap-3 rounded-2xl border border-primary/20 bg-primary/5 p-4 text-left text-sm">
              <div className="flex items-center gap-3">
                <Sparkles className="h-4 w-4 shrink-0 text-primary" />
                <span>Free chats included — no course purchase required to start</span>
              </div>
              <div className="flex items-center gap-3">
                <Shield className="h-4 w-4 shrink-0 text-primary" />
                <span>Analyze logs, files &amp; security alerts</span>
              </div>
              <div className="flex items-center gap-3">
                <Crown className="h-4 w-4 shrink-0 text-primary" />
                <span>Upgrade to Premium for unlimited conversations</span>
              </div>
            </div>
            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Button variant="ghost" onClick={() => navigate('/courses')}>
                Browse Courses
              </Button>
              <Button className="gap-2" onClick={() => navigate('/auth')}>
                <Crown className="h-4 w-4" />
                Login / Create account
              </Button>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="h-[100dvh] bg-background flex flex-col overflow-hidden">
      <Helmet>
        <title>AI Workspace | BlueTeamers</title>
        <meta name="description" content="Chat with our intelligent cybersecurity AI assistants." />
      </Helmet>

      {/* Navbar: unified top bar with brand, sidebar toggle, and model status */}
      <Navbar
        variant="floating"
        onToggleSidebar={() => setSidebarOpen(prev => !prev)}
      />

      {/* Workspace: occupies the entire viewport below the navbar; sidebar overlays it */}
      <div className="flex-1 min-h-0 relative overflow-hidden">
        <WorkspaceSidebar
          open={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          onNewChat={handleNewChat}
          conversations={convState}
          onSelectConversation={handleSelectConversation}
        />

        <main className="absolute inset-0 flex flex-col bg-zinc-950/50">
          <Chat chatState={chatState} conversations={convState} />
        </main>
      </div>
    </div>
  );
};

export default ChatPage;
