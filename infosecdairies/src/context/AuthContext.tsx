import React, { createContext, useContext, useEffect, useRef, useState } from "react";
import { apiUrl, carryOverGuestAiAllowance } from "@/services/api";
import { verifyJwtLocally } from "@/lib/jwtVerify";
import { clearGuestId, getGuestId } from "@/lib/guestId";

interface AuthUser {
  email: string;
  fullName?: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isAuthInitialized: boolean;
  login: (data: { email: string; fullName?: string; tokens?: { access?: string; refresh?: string } }) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

const REFRESH_INTERVAL_MS = 10 * 60 * 1000;
const REFRESH_LOCK_KEY = "token_refresh_lock";
const REFRESH_LOCK_TTL_MS = 15 * 1000;

/** Decode a JWT payload without verifying the signature (safe for cache-invalidation only). */
function decodeJwtUserId(token: string): number | null {
  try {
    const payloadB64 = token.split(".")[1];
    const b64 = payloadB64.replace(/-/g, "+").replace(/_/g, "/");
    const padded = b64 + "=".repeat((4 - (b64.length % 4)) % 4);
    const payload = JSON.parse(atob(padded));
    return typeof payload.user_id === "number" ? payload.user_id : null;
  } catch {
    return null;
  }
}

/**
 * Wipe all quiz scores and lesson-progress entries from localStorage.
 * Called whenever we detect a different user_id logging into the same browser
 * (i.e. the previous account was deleted and a new one created with the same email).
 */
function clearUserLocalCache() {
  const toRemove: string[] = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (!key) continue;
    if (key.startsWith("quiz_") || key.startsWith("completed_lessons_")) {
      toRemove.push(key);
    }
  }
  toRemove.forEach((k) => localStorage.removeItem(k));
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isAuthInitialized, setIsAuthInitialized] = useState(false);
  const refreshingRef = useRef(false);

  const logout = () => {
    const userEmail = localStorage.getItem("userEmail");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("userEmail");
    localStorage.removeItem("userFullName");
    // userId is intentionally NOT removed here — it must survive logout so that
    // the next login can detect a different user_id (deleted + re-registered account)
    // and wipe the stale quiz/lesson cache.
    if (userEmail) {
      localStorage.removeItem(`user_activity_log_${userEmail}`);
    }
    // Clear all cached course access tokens so the lesson gate re-checks immediately
    for (let i = sessionStorage.length - 1; i >= 0; i--) {
      const key = sessionStorage.key(i);
      if (key?.startsWith("course_access_token_")) sessionStorage.removeItem(key);
    }
    setUser(null);
  };

  const refreshAccessToken = async (): Promise<"ok" | "auth_error" | "network_error"> => {
    const lock = localStorage.getItem(REFRESH_LOCK_KEY);
    if (lock) {
      const lockTime = parseInt(lock, 10);
      if (Date.now() - lockTime < REFRESH_LOCK_TTL_MS) return "ok";
    }
    if (refreshingRef.current) return "ok";
    refreshingRef.current = true;
    localStorage.setItem(REFRESH_LOCK_KEY, String(Date.now()));

    try {
      const refreshToken = localStorage.getItem("refreshToken");
      if (!refreshToken) return "auth_error";
      const res = await fetch(apiUrl("/api/auth/token/refresh/"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken }),
      });
      // 400/401 = token genuinely invalid or blacklisted → must logout
      if (res.status === 400 || res.status === 401) return "auth_error";
      // 5xx / unexpected status = server down, Railway restarting, etc. → wait, retry later
      if (!res.ok) return "network_error";
      const data = await res.json();
      if (!data?.access) return "auth_error";
      localStorage.setItem("accessToken", data.access);
      if (data.refresh) localStorage.setItem("refreshToken", data.refresh);
      return "ok";
    } catch {
      // fetch threw = network unreachable, Railway cold start, DNS failure, etc.
      return "network_error";
    } finally {
      refreshingRef.current = false;
      localStorage.removeItem(REFRESH_LOCK_KEY);
    }
  };

  useEffect(() => {
    const storedEmail = localStorage.getItem("userEmail");
    const storedFullName = localStorage.getItem("userFullName");
    const accessToken = localStorage.getItem("accessToken");
    const refreshToken = localStorage.getItem("refreshToken");

    (async () => {
      try {
        if (storedEmail && accessToken) {
          try {
            const payload = await verifyJwtLocally(accessToken);
            if (payload.email?.toLowerCase() === storedEmail.toLowerCase()) {
              // Check if user_id matches what we stored — mismatch means the account
              // was deleted and a new one was created with the same email.
              const storedUserId = localStorage.getItem("userId");
              const tokenUserId = payload.user_id;
              if (storedUserId && tokenUserId && String(tokenUserId) !== storedUserId) {
                clearUserLocalCache();
              }
              if (tokenUserId) localStorage.setItem("userId", String(tokenUserId));
              setUser({ email: storedEmail, fullName: storedFullName || undefined });
              return;
            }
          } catch {
            // token invalid/expired — fall through to refresh
          }
        }

        if (storedEmail && refreshToken) {
          const result = await refreshAccessToken();
          if (result === "ok") {
            const newToken = localStorage.getItem("accessToken");
            if (newToken) {
              try {
                const payload = await verifyJwtLocally(newToken);
                if (payload.email?.toLowerCase() === storedEmail.toLowerCase()) {
                  const storedUserId = localStorage.getItem("userId");
                  const tokenUserId = payload.user_id;
                  if (storedUserId && tokenUserId && String(tokenUserId) !== storedUserId) {
                    clearUserLocalCache();
                  }
                  if (tokenUserId) localStorage.setItem("userId", String(tokenUserId));
                  setUser({ email: storedEmail, fullName: storedFullName || undefined });
                  return;
                }
              } catch {
                // refreshed token also invalid
              }
            }
          }
          // On startup, a network_error means the backend is unreachable — don't wipe the
          // session. The user will appear logged out but tokens are preserved; the interval
          // will recover the session once the backend comes back.
          if (result === "auth_error") logout();
        }
      } finally {
        // Auth restore is complete: either the user was restored from a stored
        // token, or there is genuinely no session. Consumers gate on this flag
        // so they never flash a "login required" screen during the brief async
        // restore that runs on first mount.
        setIsAuthInitialized(true);
      }
    })();
  }, []);

  // Periodic silent refresh + visibility-change recovery
  useEffect(() => {
    if (!user) return;

    const id = window.setInterval(async () => {
      // If the device has no internet at all, skip entirely — no reason to attempt.
      if (!navigator.onLine) return;

      // Only hit the network when the access token is actually close to expiring
      // (<10 min left). A 2-hour token does not need 12 network calls per session.
      const token = localStorage.getItem("accessToken");
      if (token) {
        try {
          const payload = await verifyJwtLocally(token);
          if (payload.exp && payload.exp > Math.floor(Date.now() / 1000) + 600) return;
        } catch { /* expired — fall through to refresh */ }
      }

      const result = await refreshAccessToken();
      // auth_error = token blacklisted / truly invalid → logout
      // network_error = Railway restarting, cold start, transient glitch → skip, retry next tick
      if (result === "auth_error") logout();
    }, REFRESH_INTERVAL_MS);

    const handleVisibility = async () => {
      if (document.visibilityState !== "visible") return;
      if (!navigator.onLine) return;

      const token = localStorage.getItem("accessToken");
      let needsRefresh = true;
      if (token) {
        try {
          await verifyJwtLocally(token);
          needsRefresh = false;
        } catch { /* expired */ }
      }
      if (needsRefresh) {
        const result = await refreshAccessToken();
        if (result === "auth_error") logout();
        // network_error → stay logged in, tokens preserved, retry when interval fires
      }
    };

    document.addEventListener("visibilitychange", handleVisibility);
    return () => {
      window.clearInterval(id);
      document.removeEventListener("visibilitychange", handleVisibility);
    };
  }, [user]);

  // Sync auth across tabs: a logout in one tab logs out all tabs, and a login
  // in another tab forces this tab to re-initialize so it never keeps showing
  // user A while the shared localStorage now holds user B's tokens (multi-tab
  // identity race).
  useEffect(() => {
    const handleStorage = (e: StorageEvent) => {
      if (e.key === "userEmail") {
        if (e.newValue === null) {
          setUser(null);
        } else if (e.newValue !== localStorage.getItem("userEmail")) {
          // Identity changed in another tab — re-read state instead of keeping
          // a stale in-memory user.
          window.location.reload();
        }
      }
      if (e.key === "accessToken" && e.newValue === null && e.oldValue) {
        setUser(null);
      }
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, []);

  const login: AuthContextValue["login"] = (data) => {
    const { email, fullName, tokens } = data;

    if (tokens?.access) {
      localStorage.setItem("accessToken", tokens.access);

      // Detect account replacement: same email, new user_id (account was deleted & re-created)
      const newUserId = decodeJwtUserId(tokens.access);
      const storedUserId = localStorage.getItem("userId");
      if (newUserId !== null) {
        if (storedUserId && String(newUserId) !== storedUserId) {
          clearUserLocalCache();
        }
        localStorage.setItem("userId", String(newUserId));
      }
    }

    if (tokens?.refresh) localStorage.setItem("refreshToken", tokens.refresh);
    localStorage.setItem("userEmail", email);
    if (fullName) {
      localStorage.setItem("userFullName", fullName);
    } else {
      localStorage.removeItem("userFullName");
    }

    // A visitor who logged in should not get a fresh daily AI allowance: carry
    // their pre-login guest usage into the authenticated account, then drop the
    // device guest id so it isn't reused for the same quota.
    const guestId = getGuestId();
    if (guestId) {
      void carryOverGuestAiAllowance(guestId).finally(clearGuestId);
    } else {
      clearGuestId();
    }

    setUser({ email, fullName });
  };

  const value: AuthContextValue = { user, isAuthenticated: !!user, isAuthInitialized, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
};
