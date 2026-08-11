/**
 * Conversations API client — Recent Conversations & Favorites.
 *
 * All requests go to the FastAPI AI service (proxied via Vite at /api/conversations).
 * The Bearer JWT is attached from localStorage so every call is user-scoped.
 */
import { apiUrl } from './api';

export interface ConversationSummary {
  conversation_id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  last_message: string;
  message_count: number;
  favorite: boolean;
  pinned: boolean;
  archived: boolean;
  conversation_type: string;
  course_id: string | null;
  course_title: string | null;
  lesson_id: string | null;
  topic: string | null;
  progress: number | null;
  assessment_id: string | null;
  assessment_score: string | null;
  tags: string[];
}

export interface ConversationMessage {
  message_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  created_at: string;
  metadata: Record<string, unknown>;
}

export interface Conversation extends ConversationSummary {
  messages: ConversationMessage[];
}

export interface ConversationListPage {
  items: ConversationSummary[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
}

export type ConversationFilter = 'all' | 'favorites' | 'recent' | 'assessment' | 'learning' | 'chat' | 'investigation' | 'tool' | 'lab';

function authHeaders(): Record<string, string> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('accessToken');
  if (token) headers['Authorization'] = `Bearer ${token}`;
  return headers;
}

async function parseError(res: Response): Promise<string> {
  try {
    const data = await res.json();
    return data.detail || data.message || `Error: ${res.status}`;
  } catch {
    return `Error: ${res.status} ${res.statusText}`;
  }
}

export async function listConversations(
  filter: ConversationFilter = 'recent',
  search?: string,
  page = 1,
  pageSize?: number,
  days?: number,
): Promise<ConversationListPage> {
  const params = new URLSearchParams({ filter, page: String(page) });
  if (search) params.set('search', search);
  if (pageSize) params.set('page_size', String(pageSize));
  if (days) params.set('days', String(days));
  const res = await fetch(apiUrl(`/api/conversations?${params}`), { headers: authHeaders() });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function searchConversations(query: string, page = 1): Promise<ConversationListPage> {
  const params = new URLSearchParams({ q: query, page: String(page) });
  const res = await fetch(apiUrl(`/api/conversations/search?${params}`), { headers: authHeaders() });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function createConversation(data: {
  first_message?: string;
  conversation_type?: string;
  course_id?: string;
  course_title?: string;
  lesson_id?: string;
  topic?: string;
}): Promise<Conversation> {
  const res = await fetch(apiUrl('/api/conversations'), {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function getConversation(id: string): Promise<Conversation> {
  const res = await fetch(apiUrl(`/api/conversations/${id}`), { headers: authHeaders() });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function updateConversation(id: string, data: {
  title?: string;
  favorite?: boolean;
  pinned?: boolean;
  archived?: boolean;
  conversation_type?: string;
  course_id?: string;
  course_title?: string;
  tags?: string[];
}): Promise<ConversationSummary> {
  const res = await fetch(apiUrl(`/api/conversations/${id}`), {
    method: 'PATCH',
    headers: authHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function deleteConversation(id: string): Promise<void> {
  const res = await fetch(apiUrl(`/api/conversations/${id}`), {
    method: 'DELETE',
    headers: authHeaders(),
  });
  if (!res.ok && res.status !== 204) throw new Error(await parseError(res));
}

export async function favoriteConversation(id: string): Promise<ConversationSummary> {
  const res = await fetch(apiUrl(`/api/conversations/${id}/favorite`), {
    method: 'POST',
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}

export async function unfavoriteConversation(id: string): Promise<ConversationSummary> {
  const res = await fetch(apiUrl(`/api/conversations/${id}/unfavorite`), {
    method: 'POST',
    headers: authHeaders(),
  });
  if (!res.ok) throw new Error(await parseError(res));
  return res.json();
}
