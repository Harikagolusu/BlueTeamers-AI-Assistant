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

export function getGuestId(): string {
  try {
    let id = localStorage.getItem(GUEST_ID_KEY);
    if (!id) {
      id = typeof crypto !== "undefined" && crypto.randomUUID ? crypto.randomUUID() : `g-${Date.now()}-${Math.random().toString(36).slice(2)}`;
      localStorage.setItem(GUEST_ID_KEY, id);
    }
    return id;
  } catch {
    return "";
  }
}

export function clearGuestId(): void {
  try {
    localStorage.removeItem(GUEST_ID_KEY);
  } catch {
    // best-effort
  }
}
