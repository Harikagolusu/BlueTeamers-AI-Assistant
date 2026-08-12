/**
 * useConversations — manages the Recent Conversations & Favorites sidebar state.
 *
 * Provides: list (paginated, filtered, searchable), favorite/unfavorite,
 * rename, delete, and open (load full history). All mutations optimistically
 * update the local list and refetch silently to stay in sync with the backend.
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import {
  listConversations,
  searchConversations,
  favoriteConversation,
  unfavoriteConversation,
  updateConversation,
  deleteConversation as apiDeleteConversation,
  getConversation,
  type ConversationSummary,
  type Conversation,
  type ConversationFilter,
  type ConversationListPage,
} from '../services/conversationsApi';

export { type ConversationSummary, type Conversation, type ConversationFilter };

export function useConversations() {
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [total, setTotal] = useState(0);
  const [hasMore, setHasMore] = useState(false);
  const [page, setPage] = useState(1);
  const [filter, setFilter] = useState<ConversationFilter>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeId, setActiveId] = useState<string | null>(null);
  const searchTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const fetchPage = useCallback(async (p: number, append = false) => {
    setLoading(true);
    setError(null);
    try {
      let result: ConversationListPage;
      if (searchQuery.trim()) {
        result = await searchConversations(searchQuery, p);
      } else {
        // Sprint 4: the sidebar shows the last 7 days of conversations
        // ("recent"); "all" and "favorites" are not time-windowed.
        const days = filter === 'recent' ? 7 : undefined;
        result = await listConversations(filter, undefined, p, undefined, days);
      }
      setConversations(prev => append ? [...prev, ...result.items] : result.items);
      setTotal(result.total);
      setHasMore(result.has_more);
      setPage(p);
    } catch (err: any) {
      setError(err.message || 'Failed to load conversations');
    } finally {
      setLoading(false);
    }
  }, [filter, searchQuery]);

  // Refetch when filter or search changes (debounced).
  useEffect(() => {
    if (searchTimer.current) clearTimeout(searchTimer.current);
    searchTimer.current = setTimeout(() => fetchPage(1), searchQuery ? 300 : 0);
    return () => { if (searchTimer.current) clearTimeout(searchTimer.current); };
  }, [filter, searchQuery, fetchPage]);

  const loadMore = useCallback(() => {
    if (hasMore && !loading) fetchPage(page + 1, true);
  }, [hasMore, loading, page, fetchPage]);

  const toggleFavorite = useCallback(async (id: string, currentFav: boolean) => {
    // Optimistic update
    setConversations(prev => prev.map(c =>
      c.conversation_id === id ? { ...c, favorite: !currentFav } : c
    ));
    try {
      if (currentFav) {
        await unfavoriteConversation(id);
      } else {
        await favoriteConversation(id);
      }
    } catch {
      // Revert on failure
      setConversations(prev => prev.map(c =>
        c.conversation_id === id ? { ...c, favorite: currentFav } : c
      ));
    }
  }, []);

  const rename = useCallback(async (id: string, title: string) => {
    const trimmed = title.trim();
    if (!trimmed) return;
    setConversations(prev => prev.map(c =>
      c.conversation_id === id ? { ...c, title: trimmed } : c
    ));
    try {
      await updateConversation(id, { title: trimmed });
    } catch (err: any) {
      setError(err.message || 'Failed to rename');
      fetchPage(1); // refetch to revert
    }
  }, [fetchPage]);

  const remove = useCallback(async (id: string) => {
    setConversations(prev => prev.filter(c => c.conversation_id !== id));
    if (activeId === id) setActiveId(null);
    try {
      await apiDeleteConversation(id);
      setTotal(t => Math.max(0, t - 1));
    } catch {
      fetchPage(1); // refetch to restore
    }
  }, [activeId, fetchPage]);

  const open = useCallback(async (id: string): Promise<Conversation | null> => {
    setActiveId(id);
    try {
      return await getConversation(id);
    } catch (err: any) {
      setError(err.message || 'Failed to open conversation');
      return null;
    }
  }, []);

  const refresh = useCallback(() => fetchPage(1), [fetchPage]);

  return {
    conversations,
    total,
    hasMore,
    loading,
    error,
    filter,
    searchQuery,
    activeId,
    setFilter,
    setSearchQuery,
    loadMore,
    toggleFavorite,
    rename,
    remove,
    open,
    refresh,
  };
}
