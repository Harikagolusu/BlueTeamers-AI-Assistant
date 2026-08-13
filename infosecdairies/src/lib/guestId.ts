/**
 * guestId.ts — a persistent device-level guest identity.
 *
 * Visitors who are not logged in still get the floating AI assistant with the
 * daily free allowance. The guest id is stored in localStorage so the same
 * browser keeps one shared allowance (and cannot silently reset it by opening
 * a new tab). It is sent to the backend as `client_id` and namespaced there as
 * a `guest:*` tracking identity.
 */

const GUEST_ID_KEY = "bt_guest_id";

// In-memory fallback so a guest always carries a non-empty id even when all
// storage is blocked (strict privacy mode). Without this the backend would
// see `client_id: ""` and treat the caller as fully anonymous, which the
// freemium service deliberately leaves unlimited/untracked — an easy bypass.
let _memoryId: string | null = null;

function _newId(): string {
  return typeof crypto !== "undefined" && crypto.randomUUID
    ? crypto.randomUUID()
    : `g-${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export function getGuestId(): string {
  try {
    let id = localStorage.getItem(GUEST_ID_KEY);
    if (!id) {
      id = _newId();
      localStorage.setItem(GUEST_ID_KEY, id);
    }
    return id;
  } catch {
    if (!_memoryId) {
      _memoryId = _newId();
    }
    return _memoryId;
  }
}

export function clearGuestId(): void {
  try {
    localStorage.removeItem(GUEST_ID_KEY);
  } catch {
    // best-effort
  }
  _memoryId = null;
}
