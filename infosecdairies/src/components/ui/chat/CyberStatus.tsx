import { useEffect, useState } from "react";

export const CYBER_STATUS_MESSAGES = [
  "Analyzing Security Events...",
  "Correlating Threat Intelligence...",
  "Processing Security Logs...",
  "Building Detection Logic...",
  "Mapping MITRE ATT&CK...",
  "Searching Knowledge Base...",
  "Parsing Indicators...",
  "Running Security Analysis...",
];

export const CYBER_STATUS_ROTATE_MS = 1400;

// Rotates through cybersecurity workstream status messages while the AI
// response is streaming. One message is shown at a time; the hook unmounts
// (and stops the timer) as soon as streaming finishes.
export function useCyberStatusMessage() {
  const [idx, setIdx] = useState(() =>
    Math.floor(Math.random() * CYBER_STATUS_MESSAGES.length),
  );

  useEffect(() => {
    const id = setInterval(
      () => setIdx((i) => (i + 1) % CYBER_STATUS_MESSAGES.length),
      CYBER_STATUS_ROTATE_MS,
    );
    return () => clearInterval(id);
  }, []);

  return CYBER_STATUS_MESSAGES[idx];
}