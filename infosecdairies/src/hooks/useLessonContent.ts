/**
 * useLessonContent
 * ────────────────
 * Fetches lesson content from the backend API instead of the static JS bundle.
 *
 * Security model
 * ─────────────
 * The backend endpoint requires:
 *   1. A valid auth JWT (IsAuthenticated)
 *   2. A current enrollment + payment record for request.user
 *
 * This means:
 *   • Content is never sent to unauthenticated callers.
 *   • A user who hasn't paid gets a 403 and null content — no bundle extraction.
 *   • Stolen course-access tokens are irrelevant here; the backend checks the
 *     auth JWT's user against the enrollment table directly.
 *
 * Caching
 * ───────
 * sessionStorage is used as an in-memory cache (cleared when the tab closes).
 * Each entry has a TTL of 1 hour, matching the server's Cache-Control: private,
 * max-age=3600 header.  This avoids a round-trip on every lesson navigation
 * while ensuring stale content doesn't persist across sessions.
 *
 * Usage
 * ─────
 *   const { lessonContent, contentLoading, contentError } = useLessonContent(
 *     slug,
 *     lessonId,
 *     accessState,   // from useCourseAccess — only fetch when "granted"
 *   );
 */

import { useState, useEffect, useRef } from "react";
import { apiUrl } from "@/services/api";
import type { LessonContent } from "@/data/lessonContent";

const CACHE_KEY = (slug: string, lessonId: string) =>
  `lc_v2_${slug}_${lessonId}`;

const CACHE_TTL_MS = 60 * 60 * 1000; // 1 hour

interface CacheEntry {
  data: LessonContent;
  expires: number;
}

function readCache(slug: string, lessonId: string): LessonContent | null {
  try {
    const raw = sessionStorage.getItem(CACHE_KEY(slug, lessonId));
    if (!raw) return null;
    const entry: CacheEntry = JSON.parse(raw);
    if (entry.expires < Date.now()) {
      sessionStorage.removeItem(CACHE_KEY(slug, lessonId));
      return null;
    }
    return entry.data;
  } catch {
    return null;
  }
}

function writeCache(slug: string, lessonId: string, data: LessonContent) {
  try {
    const entry: CacheEntry = { data, expires: Date.now() + CACHE_TTL_MS };
    sessionStorage.setItem(CACHE_KEY(slug, lessonId), JSON.stringify(entry));
  } catch {
    // sessionStorage full — not fatal, just skip the cache write.
  }
}

export function useLessonContent(
  slug: string | undefined,
  lessonId: string | undefined,
  /** Pass accessState from useCourseAccess — prevents unnecessary 403s. */
  accessState: "loading" | "granted" | "denied" | "unauthenticated",
): {
  lessonContent: LessonContent | null;
  contentLoading: boolean;
  contentError: boolean;
} {
  const [lessonContent, setLessonContent] = useState<LessonContent | null>(null);
  const [contentLoading, setContentLoading] = useState(true);
  const [contentError, setContentError] = useState(false);

  // Track the last fetched (slug, lessonId) pair so we don't show stale content
  // from the previous lesson while the new one is loading.
  const lastFetchRef = useRef<string>("");

  useEffect(() => {
    // Don't attempt a fetch until the course access gate has resolved.
    if (accessState === "loading") return;

    if (!slug || !lessonId || accessState !== "granted") {
      setLessonContent(null);
      setContentLoading(false);
      setContentError(accessState === "denied" || accessState === "unauthenticated");
      return;
    }

    const fetchKey = `${slug}::${lessonId}`;

    // Serve from cache if available and fresh.
    const cached = readCache(slug, lessonId);
    if (cached) {
      lastFetchRef.current = fetchKey;
      setLessonContent(cached);
      setContentLoading(false);
      setContentError(false);
      return;
    }

    // Show loading state only when switching to a different lesson.
    if (lastFetchRef.current !== fetchKey) {
      setContentLoading(true);
      setLessonContent(null);
      setContentError(false);
    }

    const authToken = localStorage.getItem("accessToken");
    if (!authToken) {
      setContentLoading(false);
      setContentError(true);
      return;
    }

    let cancelled = false;

    (async () => {
      try {
        const res = await fetch(
          apiUrl(`/api/courses/${slug}/lessons/${lessonId}/content/`),
          {
            headers: { Authorization: `Bearer ${authToken}` },
            // Tell the browser to use its own HTTP cache for repeat navigations
            // within the same session (Cache-Control: private, max-age=3600
            // is set by the server).
            cache: "default",
          },
        );

        if (cancelled) return;

        if (res.status === 401) {
          // Auth token expired — clear stale tokens; useCourseAccess will redirect.
          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");
          localStorage.removeItem("userEmail");
          setContentError(true);
          setContentLoading(false);
          return;
        }

        if (!res.ok) {
          // 403 = not enrolled / not paid (shouldn't happen if accessState === "granted",
          // but handle it defensively).
          setContentError(true);
          setContentLoading(false);
          return;
        }

        const data: LessonContent = await res.json();
        if (cancelled) return;

        writeCache(slug, lessonId, data);
        lastFetchRef.current = fetchKey;
        setLessonContent(data);
        setContentLoading(false);
        setContentError(false);
      } catch {
        if (!cancelled) {
          setContentError(true);
          setContentLoading(false);
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [slug, lessonId, accessState]);

  return { lessonContent, contentLoading, contentError };
}
