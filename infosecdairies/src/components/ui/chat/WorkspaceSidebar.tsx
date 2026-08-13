import React, { useState } from 'react';
import {
  MessageSquarePlus,
  Search,
  Trash2,
  PenLine,
  Check,
  X,
  MessageSquare,
  Clock,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import logo from '@/assets/logo.png';
import type { useConversations } from '@/hooks/useConversations';

export interface WorkspaceSidebarProps {
  open?: boolean;
  onClose?: () => void;
  onNewChat?: () => void;
  conversations?: ReturnType<typeof useConversations>;
  onSelectConversation?: (id: string) => void;
}

type FilterTab = 'recent' | 'favorites' | 'all';

const FILTER_TABS: { key: FilterTab; label: string }[] = [
  { key: 'favorites', label: 'Favorites' },
  { key: 'all', label: 'All' },
];

function relativeTime(iso: string): string {
  const then = new Date(iso).getTime();
  if (!Number.isFinite(then)) return '';
  const diffMs = Date.now() - then;
  const mins = Math.floor(diffMs / 60000);
  if (mins < 1) return 'now';
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days}d ago`;
  return new Date(then).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

// Timeline grouping for the history list: Today, Yesterday, Last 7 Days,
// Older. Items loaded via "Load more" fall into the correct group too.
function timelineGroup(iso: string): string {
  const then = new Date(iso);
  if (isNaN(then.getTime())) return 'Older';
  const now = new Date();
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const startOfYesterday = new Date(startOfToday);
  startOfYesterday.setDate(startOfYesterday.getDate() - 1);
  const startOfLast7 = new Date(startOfToday);
  startOfLast7.setDate(startOfLast7.getDate() - 6);
  if (then >= startOfToday) return 'Today';
  if (then >= startOfYesterday) return 'Yesterday';
  if (then >= startOfLast7) return 'Last 7 Days';
  return 'Older';
}

const TIMELINE_ORDER = ['Today', 'Yesterday', 'Last 7 Days', 'Older'];

export const WorkspaceSidebar = ({
  open = false,
  onClose,
  onNewChat,
  conversations,
  onSelectConversation,
}: WorkspaceSidebarProps) => {
  const conv = conversations;
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');

  const handleNewChat = () => {
    onNewChat?.();
    onClose?.();
  };

  const startRename = (id: string, title: string) => {
    setEditingId(id);
    setEditTitle(title);
  };

  const commitRename = (id: string) => {
    if (editTitle.trim()) conv?.rename(id, editTitle);
    setEditingId(null);
    setEditTitle('');
  };

  const confirmDelete = (id: string, title: string) => {
    if (window.confirm(`Delete "${title}"?`)) conv?.remove(id);
  };

  const switchFilter = (tab: FilterTab) => {
    conv?.setFilter(tab);
  };

  const handleSelect = (id: string) => {
    if (editingId === id) return;
    onSelectConversation?.(id);
  };

  return (
    <>
      {/* Backdrop */}
      {open && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Drawer */}
      <div
        role="dialog"
        aria-label="Workspace navigation"
        aria-modal={open}
        className={`flex flex-col bg-zinc-950/95 border-r border-border backdrop-blur-xl fixed inset-y-0 left-0 z-50 w-full sm:w-72 overflow-hidden transform transition-transform duration-300 ease-in-out ${
          open ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex flex-col h-full">
          {/* Brand header */}
          <div className="flex items-center gap-3 px-4 py-4 border-b border-border/50">
            <img src={logo} alt="BlueTeamers" className="h-9 w-9 object-contain" />
            <div className="min-w-0 leading-tight">
              <div className="flex items-center gap-1.5">
                <span className="font-semibold text-sm text-foreground truncate">
                  BlueTeamers <span className="gradient-text">AI</span>
                </span>
                <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-primary/10 border border-primary/20 text-primary font-mono shrink-0">
                  WORKSPACE
                </span>
              </div>
              <p className="text-[10px] font-mono text-muted-foreground truncate">
                Security learning companion
              </p>
            </div>
          </div>

          {/* New Chat - primary action */}
          <div className="p-3 border-b border-border/50 z-10">
            <Button
              className="w-full justify-center gap-2 h-10 bg-primary/15 hover:bg-primary/25 text-primary border border-primary/40 shadow-[0_0_12px_rgba(0,186,216,0.15)] transition-all"
              onClick={handleNewChat}
            >
              <MessageSquarePlus className="w-4 h-4" />
              New Chat
            </Button>
          </div>

          {/* Search */}
          {conv && (
            <div className="px-3 pt-3">
              <div className="relative">
                <Search className="w-4 h-4 text-muted-foreground absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
                <Input
                  value={conv.searchQuery}
                  onChange={(e) => conv.setSearchQuery(e.target.value)}
                  placeholder="Search conversations..."
                  className="h-6 min-h-0 py-0 pl-9 text-[11px] bg-zinc-900/80 border-border/60"
                  style={{ height: 24 }}
                />
              </div>
            </div>
          )}

          {/* Filter tabs */}
          {conv && (
            <div className="flex items-center gap-1 px-3 pt-2">
              {FILTER_TABS.map((tab) => {
                const active = conv.filter === tab.key;
                return (
                  <button
                    key={tab.key}
                    onClick={() => switchFilter(tab.key)}
                    className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition-colors ${
                      active
                        ? 'bg-primary/15 text-primary border border-primary/30'
                        : 'text-muted-foreground hover:text-foreground hover:bg-zinc-900 border border-transparent'
                    }`}
                  >
                    {tab.label}
                  </button>
                );
              })}
            </div>
          )}

          {/* Conversation list */}
          {conv && (
            <ScrollArea className="flex-1 min-h-0 px-2 py-2">
              {conv.loading && conv.conversations.length === 0 ? (
                <div className="px-3 py-6 text-center">
                  <p className="text-[11px] text-muted-foreground font-mono animate-pulse">
                    Loading conversations...
                  </p>
                </div>
              ) : conv.conversations.length === 0 ? (
                <div className="px-3 py-6 text-center">
                  <MessageSquare className="w-5 h-5 mx-auto text-muted-foreground/50 mb-2" />
                  <p className="text-[11px] text-muted-foreground">
                    {conv.searchQuery
                      ? 'No conversations match your search.'
                      : 'No conversations yet. Start a new chat to begin.'}
                  </p>
                </div>
              ) : (
                <div className="flex flex-col gap-1">
                  {(() => {
                    const groups = TIMELINE_ORDER
                      .map((label) => ({
                        label,
                        items: conv.conversations.filter((c) => timelineGroup(c.updated_at) === label),
                      }))
                      .filter((g) => g.items.length > 0);
                    return groups.map((group) => (
                      <div key={group.label} className="flex flex-col gap-1 mb-2">
                        <div className="px-3 pt-2 pb-1 text-[10px] font-mono uppercase tracking-widest text-muted-foreground/70">
                          {group.label}
                        </div>
                        {group.items.map((c) => {
                          const active = conv.activeId === c.conversation_id;
                          const isEditing = editingId === c.conversation_id;
                          return (
                            <div
                              key={c.conversation_id}
                              onClick={() => handleSelect(c.conversation_id)}
                              className={`group relative flex flex-col gap-0.5 rounded-lg px-3 py-2.5 cursor-pointer border transition-colors ${
                                active
                                  ? 'bg-primary/10 border-primary/30'
                                  : 'border-transparent hover:bg-zinc-900/80'
                              }`}
                            >
                              {isEditing ? (
                                <div
                                  className="flex items-center gap-1.5"
                                  onClick={(e) => e.stopPropagation()}
                                >
                                  <Input
                                    autoFocus
                                    value={editTitle}
                                    onChange={(e) => setEditTitle(e.target.value)}
                                    onKeyDown={(e) => {
                                      if (e.key === 'Enter') commitRename(c.conversation_id);
                                      if (e.key === 'Escape') setEditingId(null);
                                    }}
                                    className="h-7 text-xs bg-zinc-900/90 border-border/60"
                                  />
                                  <button
                                    onClick={() => commitRename(c.conversation_id)}
                                    className="text-primary hover:text-primary/80"
                                    aria-label="Save title"
                                  >
                                    <Check className="w-3.5 h-3.5" />
                                  </button>
                                  <button
                                    onClick={() => setEditingId(null)}
                                    className="text-muted-foreground hover:text-foreground"
                                    aria-label="Cancel rename"
                                  >
                                    <X className="w-3.5 h-3.5" />
                                  </button>
                                </div>
                              ) : (
                                <>
                                  <div className="flex items-start gap-2 min-w-0">
                                    <div className="flex items-center gap-1.5 min-w-0 flex-1">
                                      <span className="text-xs font-medium text-foreground truncate">
                                        {c.title || 'Untitled'}
                                      </span>
                                    </div>
                                    <span className="flex items-center gap-1 text-[9px] font-mono text-muted-foreground shrink-0">
                                      <Clock className="w-3 h-3" />
                                      {relativeTime(c.updated_at)}
                                    </span>
                                  </div>

                                  {/* Row actions: rename, delete */}
                                  <div
                                    className="absolute right-1.5 top-1.5 hidden group-hover:flex items-center gap-0.5 bg-zinc-950/90 rounded-md border border-border/60 p-0.5"
                                    onClick={(e) => e.stopPropagation()}
                                  >
                                    <button
                                      onClick={() => startRename(c.conversation_id, c.title)}
                                      className="p-1 rounded hover:bg-zinc-800 text-muted-foreground"
                                      aria-label="Rename"
                                    >
                                      <PenLine className="w-3 h-3" />
                                    </button>
                                    <button
                                      onClick={() => confirmDelete(c.conversation_id, c.title)}
                                      className="p-1 rounded hover:bg-zinc-800 text-muted-foreground hover:text-red-400"
                                      aria-label="Delete"
                                    >
                                      <Trash2 className="w-3 h-3" />
                                    </button>
                                  </div>
                                </>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    ));
                  })()}

                  {conv.hasMore && (
                    <Button
                      variant="ghost"
                      size="sm"
                      className="mt-1 text-[11px] text-muted-foreground hover:text-primary"
                      onClick={conv.loadMore}
                      disabled={conv.loading}
                    >
                      {conv.loading ? 'Loading...' : 'Load more'}
                    </Button>
                  )}
                </div>
              )}
            </ScrollArea>
          )}

          {/* Footer removed: user details bar omitted from the AI workspace
              sidebar for a cleaner, minimal layout. */}
        </div>
      </div>
    </>
  );
};
