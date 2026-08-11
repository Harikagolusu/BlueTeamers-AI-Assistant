import React, { useRef, useEffect } from 'react';
import { User, Trash2, Sparkles, Star } from 'lucide-react';
import logo from '@/assets/logo.png';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { ChatInput } from './chat/ChatInput';
import { ChatMarkdown } from './chat/ChatMarkdown';
import { EmptyStateDashboard } from './chat/EmptyStateDashboard';
import { DashboardLoading } from './chat/DashboardLoading';
import { ProfileCard, ProgressCard, EnrolledCoursesCard, RecommendationCard, CourseCard, SuggestedCourseCard } from './chat/PlatformCards';
import { QuizCard, QuizOfferCard, QuizResultCard } from './chat/QuizCard';
import { LabCard } from './chat/LabCard';
import { consumeLogAnalysis } from '@/lib/logAnalysis';
import { buildLabStartContext, getPracticeLab } from '@/lib/labContext';
import { useChat, type ChatMessage } from '@/hooks/useChat';
import { useConversations } from '@/hooks/useConversations';

export interface ChatProps {
  chatState?: ReturnType<typeof useChat>;
  conversations?: ReturnType<typeof useConversations>;
}

export const Chat = ({ chatState, conversations }: ChatProps) => {
    const chat = chatState ?? useChat();
  const { messages, sendMessage, sendLabHint, isLoading, error, stopGenerating, clearMessages, initializeSession, conversationId, language, setLanguage } = chat;
  const conv = conversations;

  const activeConversation = conv?.conversations.find(
    (c) => c.conversation_id === conversationId,
  );
  const isFavorite = !!activeConversation?.favorite;

  const handleToggleFavorite = () => {
    if (!conv || !conversationId) return;
    conv.toggleFavorite(conversationId, isFavorite);
  };
  const scrollRef = useRef<HTMLDivElement>(null);
  const pendingAnalysisHandled = useRef(false);
  const nearBottomRef = useRef(true);

  useEffect(() => {
    const viewport = scrollRef.current?.querySelector('[data-radix-scroll-area-viewport]');
    if (!viewport) return;
    const onScroll = () => {
      const el = viewport as HTMLElement;
      nearBottomRef.current = el.scrollHeight - el.scrollTop - el.clientHeight < 160;
    };
    viewport.addEventListener('scroll', onScroll, { passive: true });
    return () => viewport.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    // Only auto-scroll during an active conversation. The initial empty-state
    // dashboard must stay pinned to the top while it loads.
    const hasUserMessage = messages.some(m => m.role === 'user');
    if (!hasUserMessage) return;
    const viewport = scrollRef.current?.querySelector('[data-radix-scroll-area-viewport]');
    if (viewport && nearBottomRef.current) {
      viewport.scrollTop = viewport.scrollHeight;
    }
  }, [messages, isLoading]);

  useEffect(() => {
    initializeSession();
  }, [initializeSession]);

  // Hand off a queued analysis (e.g. "Analyze with AI" from the Log Explorer)
  // once session initialization settles, so the message order stays clean.
  useEffect(() => {
    if (pendingAnalysisHandled.current) return;
    if (isLoading) return;
    const pending = consumeLogAnalysis();
    if (!pending) return;
    pendingAnalysisHandled.current = true;
        sendMessage(pending.text, pending.files);
  }, [isLoading, sendMessage]);

  const handleQuickPrompt = (prompt: string) => {
    sendMessage(prompt);
  };

  const handleLabAnswer = (answer: string) => sendMessage(answer);
  const handleLabHint = () => sendLabHint();
  const handleLabRestart = (labId: string) => {
    const lab = getPracticeLab(labId);
    sendMessage(
      `Restart the ${lab?.title || labId} practice lab`,
      undefined,
      undefined,
      buildLabStartContext(labId),
    );
  };

  // Determine if we should show the empty state dashboard
  // We show it if there are no user messages yet.
  const hasUserMessage = messages.some(m => m.role === 'user');
  const sessionInitMessage = messages.length > 0 && messages[0].metadata?.platform?.context ? messages[0] : null;

  // While the assistant response has not produced content yet, hide the empty
  // placeholder bubble and show a single BlueTeamers logo + streaming dots as
  // the only loading indicator.
  const lastMsg = messages[messages.length - 1];
  const isStreamingAssistant = Boolean(
    isLoading && lastMsg?.role === 'assistant' && !lastMsg.content,
  );
  const showTypingIndicator =
    isLoading && (isStreamingAssistant || !lastMsg || lastMsg.role !== 'assistant');

  return (
    <div className="flex flex-col flex-1 min-h-0 w-full overflow-hidden relative">
      {/* Main Chat Area */}
      <div className="flex-1 min-h-0 relative overflow-hidden bg-dot-pattern bg-[size:20px_20px]">
        {/* Decorative Gradients */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-[120px] pointer-events-none"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-emerald-500/5 rounded-full blur-[120px] pointer-events-none"></div>

        {/* Favorite + Clear conversation (floating, does not add a header bar) */}
        {messages.length > 1 && (
          <div className="absolute top-3 right-3 z-20 flex items-center gap-2">
            {conversationId && (
              <Button
                variant="outline"
                size="icon"
                onClick={handleToggleFavorite}
                title={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                aria-label={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
                className={`h-9 w-9 rounded-lg border-border bg-background/60 backdrop-blur-md transition-all duration-300 ${
                  isFavorite
                    ? 'text-amber-400 border-amber-400/40 hover:bg-amber-400/10'
                    : 'hover:text-amber-400 hover:border-amber-400/40'
                }`}
              >
                <Star className={`w-4 h-4 ${isFavorite ? 'fill-amber-400' : ''}`} />
              </Button>
            )}
            <Button
              variant="outline"
              size="icon"
              onClick={clearMessages}
              title="Clear Conversation"
              className="h-9 w-9 rounded-lg border-border bg-background/60 backdrop-blur-md hover:bg-destructive/10 hover:text-destructive hover:border-destructive/30 transition-all duration-300"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          </div>
        )}
        
        <ScrollArea className="h-full w-full z-10" ref={scrollRef}>
          {!hasUserMessage && isLoading && !sessionInitMessage ? (
            <DashboardLoading />
          ) : (
          <div className="flex flex-col gap-4 sm:gap-6 max-w-4xl mx-auto pb-32 sm:pb-40 px-3 sm:px-6 md:px-8 py-4 sm:py-6">
            
            {/* Show Empty State Dashboard if no user interaction yet */}
            {!hasUserMessage && sessionInitMessage && sessionInitMessage.metadata?.platform?.context && (
              <EmptyStateDashboard 
                platformContext={sessionInitMessage.metadata.platform.context} 
                onQuickPrompt={handleQuickPrompt}
              />
            )}

            {/* If there are user messages, optionally show the Welcome message as a text block, 
                or just skip it. We'll skip rendering the raw sessionInitMessage bubble if we showed the dashboard above it. 
                Actually, we render all messages AFTER the init message. */}
            
            {messages.map((msg, idx) => {
              // Skip rendering the very first initialization message as a bubble, because we either:
              // 1. Show it as the Dashboard above (if no user messages)
              // 2. Hide it completely to keep the chat clean once they start talking
              if (idx === 0 && msg.metadata?.platform?.context) {
                return null; 
              }

              // Hide the empty streaming placeholder bubble — the BlueTeamers
              // logo + dots typing indicator is shown instead while loading.
              if (isStreamingAssistant && idx === messages.length - 1) {
                return null;
              }

              const assessment = msg.metadata?.assessment;
              const quizMode = assessment && (assessment.mode === 'started' || assessment.mode === 'next');
              const labActive = !!(msg.metadata?.lab?.active);
              const isStreamingMsg = isLoading && idx === messages.length - 1;

              return (
                <div key={idx} className={`flex gap-2.5 sm:gap-4 animate-in fade-in slide-in-from-bottom-2 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  {/* Avatar */}
                  <div className={`w-7 h-7 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center shrink-0 border transition-all mt-1 ${
                    msg.role === 'user' 
                      ? 'bg-primary/20 border-primary/40 text-primary shadow-[0_0_10px_rgba(0,186,216,0.1)]' 
                      : 'bg-zinc-900 border-zinc-700 text-foreground'
                  }`}>
                    {msg.role === 'user' ? <User className="w-4 h-4" /> : <img src={logo} alt="BlueTeamers" className="w-full h-full rounded-md object-contain" />}
                  </div>

                  {/* Message Content */}
                  <div className={`flex flex-col max-w-[92%] sm:max-w-[85%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                    <div className={`rounded-2xl p-3 sm:p-4 shadow-sm border ${
                      msg.role === 'user'
                        ? 'bg-primary/10 border-primary/20 text-foreground rounded-tr-sm'
                        : 'bg-zinc-900/80 backdrop-blur-sm border-zinc-800 text-zinc-100 rounded-tl-sm prose prose-zinc prose-invert prose-sm max-w-none shadow-[0_0_15px_rgba(0,0,0,0.2)]'
                    }`}>
                      <div>
                        {msg.role === 'user' ? (
                          <p className="bt-mono whitespace-pre-wrap text-sm leading-relaxed">{msg.content || "Uploaded files:"}</p>
                        ) : quizMode ? (
                          <QuizCard
                            quiz={assessment?.quiz}
                            disabled={isLoading}
                            onAnswer={(answer: string) => sendMessage(answer)}
                          />
                        ) : labActive ? (
                          <>
                            {msg.content ? (
                              <div className="bt-cyber-message mb-3">
                                <ChatMarkdown isStreaming={isStreamingMsg}>{msg.content}</ChatMarkdown>
                              </div>
                            ) : null}
                            <LabCard
                              lab={msg.metadata.lab}
                              disabled={isLoading}
                              onAnswer={handleLabAnswer}
                              onHint={handleLabHint}
                              onRestart={() => handleLabRestart(msg.metadata.lab.lab_id)}
                            />
                          </>
                        ) : (
                          <div className="bt-cyber-message">
                            <ChatMarkdown isStreaming={isStreamingMsg}>{msg.content}</ChatMarkdown>
                          </div>
                        )}
                      </div>

                      {/* Assessment offer card (shown under the answer) */}
                      {msg.role === 'assistant' && assessment?.mode === 'offered' && (
                        <div className="mt-4 pt-3 border-t border-border/50 not-prose">
                          <QuizOfferCard
                            topic={assessment.topic}
                            disabled={isLoading}
                            onStart={() => sendMessage('yes')}
                            onSkip={() => sendMessage('no thanks')}
                          />
                        </div>
                      )}

                      {/* Assessment summary card (shown under the summary text) */}
                      {msg.role === 'assistant' && assessment?.mode === 'summary' && assessment?.result && (
                        <div className="mt-4 pt-3 border-t border-border/50 not-prose">
                          <QuizResultCard
                            result={assessment.result}
                            disabled={isLoading}
                            onRetake={() => sendMessage('another quiz')}
                          />
                        </div>
                      )}

                      {/* User Attachments Preview inside Bubble */}
                      {msg.role === 'user' && msg.metadata?.attachments && msg.metadata.attachments.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-3 pt-3 border-t border-primary/10">
                          {msg.metadata.attachments.map((att: { name: string; type: string; content: string }, attIdx: number) => (
                            <div key={attIdx} className="rounded-lg overflow-hidden border border-primary/20 bg-zinc-950/50">
                              {att.type.startsWith('image/') ? (
                                <img src={att.content} alt={att.name} className="max-h-32 max-w-[200px] object-contain p-1" />
                              ) : (
                                <div className="px-2 py-1 flex items-center gap-2 text-[10px] font-mono text-muted-foreground">
                                  <span>{att.name}</span>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      )}

                      {/* AI Structured Platform Cards (returned by Platform Engine) */}
                      {msg.role === 'assistant' && msg.metadata?.platform?.cards && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-4 not-prose">
                          {msg.metadata.platform.cards.map((card: { type: string; data: Record<string, unknown>; actions?: unknown[] }, cIdx: number) => {
                            if (card.type === 'course_recommendation') {
                              return <RecommendationCard key={cIdx} recommendations={[card.data]} />;
                            }
                            if (card.type === 'progress_snapshot') {
                              return <ProgressCard key={cIdx} progress={[card.data]} courses={[]} />;
                            }
                            if (card.type === 'course' || (card.actions && card.actions.length > 0)) {
                              return <CourseCard key={cIdx} card={card} />;
                            }
                            return null;
                          })}
                        </div>
                      )}

                      {/* Suggested BlueTeamers Courses: smart course recommendations
                          based on the topic of the answer. Only rendered on a strong
                          topic match (never after every response). */}
                      {msg.role === 'assistant' && msg.metadata?.suggested_courses && msg.metadata.suggested_courses.length > 0 && (
                        <div className="mt-4 pt-3 border-t border-border/50 not-prose">
                          <div className="flex items-center gap-2 mb-3">
                            <Sparkles className="w-4 h-4 text-primary" />
                            <h4 className="text-xs font-mono text-muted-foreground uppercase tracking-widest">
                              Suggested BlueTeamers Courses
                            </h4>
                          </div>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {msg.metadata.suggested_courses.slice(0, 3).map((s: any, sIdx: number) => (
                              <SuggestedCourseCard key={sIdx} suggestion={s} />
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
            
            {/* Typing / Loading indicator — a single BlueTeamers logo + dots */}
            {showTypingIndicator && <TypingIndicator />}

            {error && (
              <div className="text-destructive text-center p-3 text-xs bg-destructive/10 border border-destructive/20 rounded-xl font-mono mx-auto max-w-md">
                SYSTEM EXCEPTION: {error}
              </div>
            )}
          </div>
          )}
        </ScrollArea>
        
        {/* Input Area (Pinned to bottom) */}
        <div className="absolute bottom-0 left-0 right-0 px-2 sm:px-4 pt-4 pb-[max(0.5rem,env(safe-area-inset-bottom))] sm:pb-4 bg-gradient-to-t from-background via-background/90 to-transparent z-20 pointer-events-none">
          <div className="max-w-3xl mx-auto pointer-events-auto shadow-2xl rounded-2xl relative">
            <ChatInput 
                            onSendMessage={(text, attachments) => sendMessage(text, attachments)}
              onStop={stopGenerating}
              isLoading={isLoading}
              language={language}
              onLanguageChange={setLanguage}
            />
            <div className="text-center mt-2">
              <span className="text-[10px] text-muted-foreground font-mono">
                AI Assistant can make mistakes. Verify important security information.
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const TypingIndicator = () => {
  return (
    <div className="flex gap-4 items-end animate-fade-in">
      <div className="relative w-8 h-8 shrink-0 overflow-hidden rounded-lg border border-primary/30 shadow-[0_0_15px_rgba(0,186,216,0.2)] animate-pulse-glow">
        <img src={logo} alt="BlueTeamers" className="h-full w-full object-cover" />
        <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-emerald-400 animate-pulse-glow" />
      </div>
      <div className="flex items-center gap-1 px-4 py-3 rounded-2xl rounded-bl-sm bg-zinc-900/50 border border-zinc-800">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="w-1.5 h-1.5 rounded-full bg-primary animate-dot-pulse"
            style={{ animationDelay: `${i * 0.2}s` }}
          />
        ))}
      </div>
    </div>
  );
};
