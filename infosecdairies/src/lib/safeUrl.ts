// Guards against XSS via `javascript:` / `data:` URLs in content-controlled
// hrefs (lesson resources, chat links). Only http/https/mailto are allowed;
// everything else resolves to "#" so a malicious value can never execute.
const SAFE_PROTOCOLS = ["http:", "https:", "mailto:"];

export function safeUrl(raw: string | null | undefined): string {
  if (!raw) return "#";
  const value = String(raw).trim();
  // Reject values with embedded whitespace/control tricks (e.g. "java\nscript:")
  // and any leading protocol that isn't in the whitelist.
  if (/\s/.test(value)) return "#";
  const match = value.match(/^([a-zA-Z][a-zA-Z0-9+.-]*):/);
  if (match && !SAFE_PROTOCOLS.includes(match[1].toLowerCase())) {
    return "#";
  }
  return value;
}