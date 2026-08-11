export const PENDING_ANALYSIS_KEY = "bt_pending_log_analysis_v1";

export interface PendingAnalysis {
  text: string;
  files: Array<{ name: string; type: string; content: string }>;
}

export function queueLogAnalysis(text: string, files: PendingAnalysis["files"]): void {
  try {
    sessionStorage.setItem(PENDING_ANALYSIS_KEY, JSON.stringify({ text, files }));
  } catch {
    // sessionStorage may be unavailable; the handoff is best-effort.
  }
}

export function consumeLogAnalysis(): PendingAnalysis | null {
  try {
    const raw = sessionStorage.getItem(PENDING_ANALYSIS_KEY);
    if (!raw) return null;
    sessionStorage.removeItem(PENDING_ANALYSIS_KEY);
    return JSON.parse(raw) as PendingAnalysis;
  } catch {
    return null;
  }
}
