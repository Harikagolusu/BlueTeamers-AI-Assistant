/**
 * useAiAccess — fetch and cache the freemium access status from the AI backend
 * (`GET /api/chat/access`). Free users see their daily remaining message count;
 * premium users are unlimited. On any error the status fails open (treated as
 * unlimited) so the assistant is never blocked by a flaky status endpoint.
 */

import { useCallback, useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { apiUrl } from "@/services/api";
import { getGuestId } from "@/lib/guestId";

export interface AiAccessStatus {
  access_level: "premium" | "free";
  is_premium: boolean;
  enabled: boolean;
  limit: number;
  used: number;
  remaining: number;
  reset_at: string | null;
}

export interface UseAiAccessResult {
  status: AiAccessStatus | null;
  loading: boolean;
  refresh: () => Promise<void>;
}

export function useAiAccess(): UseAiAccessResult {
  const { isAuthenticated } = useAuth();
  const [status, setStatus] = useState<AiAccessStatus | null>(null);
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    const accessToken = localStorage.getItem("accessToken");
    setLoading(true);
    try {
      // Authenticated users are identified by the JWT; guests (not logged in)
      // are identified by a persistent device-level client id so they too get
      // the daily free allowance.
      const query = accessToken
        ? ""
        : `?client_id=${encodeURIComponent(getGuestId())}`;
      const res = await fetch(apiUrl(`/api/chat/access${query}`), {
        headers: accessToken
          ? { Authorization: `Bearer ${accessToken}` }
          : {},
      });
      if (!res.ok) {
        setStatus(null);
        return;
      }
      const data = (await res.json()) as AiAccessStatus;
      setStatus({
        access_level: data.access_level,
        is_premium: !!data.is_premium,
        enabled: !!data.enabled,
        limit: Number(data.limit) || 0,
        used: Number(data.used) || 0,
        remaining: Number(data.remaining) || 0,
        reset_at: data.reset_at || null,
      });
    } catch {
      setStatus(null);
    } finally {
      setLoading(false);
    }
  }, []);

  // Always fetch: the assistant is available without login too (guests share
  // the free allowance via their client id). Re-fetch when the auth state flips
  // so the status reflects the current identity.
  useEffect(() => {
    refresh();
  }, [isAuthenticated, refresh]);

  return { status, loading, refresh };
}
