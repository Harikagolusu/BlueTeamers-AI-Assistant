import { useState, useEffect, useRef } from "react";

export const useRealtimeSimulation = (intervalMs = 5000) => {
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setTick((t) => t + 1), intervalMs);
    return () => clearInterval(id);
  }, [intervalMs]);

  return tick;
};

export const useAnimatedValue = (target: number, duration = 800) => {
  const [value, setValue] = useState(target);
  const rafRef = useRef<number>();

  useEffect(() => {
    const start = value;
    const diff = target - start;
    if (diff === 0) return;

    const startTime = performance.now();
    const animate = (now: number) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setValue(Math.round(start + diff * eased));
      if (progress < 1) {
        rafRef.current = requestAnimationFrame(animate);
      }
    };
    rafRef.current = requestAnimationFrame(animate);
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, [target, duration]);

  return value;
};

export const randomVariation = (base: number, percent = 10) => {
  const delta = Math.round(base * (percent / 100));
  return base + Math.floor(Math.random() * (delta * 2 + 1)) - delta;
};

const alertNames = [
  "Suspicious PowerShell Execution",
  "Failed Login Attempt (5x)",
  "Unusual Outbound Traffic",
  "Port Scan Detected",
  "DNS Query to Suspicious Domain",
  "New Service Installed",
  "Scheduled Task Created",
  "Credential Dump Detected",
  "Brute Force Attempt",
  "Lateral Movement via PsExec",
  "Malicious File Download",
  "Registry Key Modified",
  "Privilege Escalation Attempt",
  "Data Exfiltration Alert",
  "Unauthorized RDP Session",
];

const analystNames = ["Sarah M.", "John D.", "Mike R.", "Lisa K.", "Alex T."];
const severities = ["Critical", "High", "Medium", "Low"] as const;
const sources = ["WKS-PC-0127", "192.168.1.105", "10.0.0.42", "SRV-DB-01", "172.16.0.88", "admin_user"];

export type LiveEvent = {
  id: string;
  timestamp: Date;
  type: "alert" | "action" | "status";
  message: string;
  severity?: string;
  analyst?: string;
};

export const useActivityFeed = (maxEvents = 20) => {
  const [events, setEvents] = useState<LiveEvent[]>(() => generateInitialEvents());
  const counterRef = useRef(10);

  useEffect(() => {
    const id = setInterval(() => {
      setEvents((prev) => {
        const newEvent = generateRandomEvent(counterRef.current++);
        return [newEvent, ...prev].slice(0, maxEvents);
      });
    }, 4000 + Math.random() * 6000);
    return () => clearInterval(id);
  }, [maxEvents]);

  return events;
};

function generateInitialEvents(): LiveEvent[] {
  const events: LiveEvent[] = [];
  for (let i = 0; i < 8; i++) {
    events.push(generateRandomEvent(i, i * 30));
  }
  return events;
}

function generateRandomEvent(id: number, secondsAgo = 0): LiveEvent {
  const type = ["alert", "action", "status"][Math.floor(Math.random() * 3)] as LiveEvent["type"];
  const timestamp = new Date(Date.now() - secondsAgo * 1000);
  const analyst = analystNames[Math.floor(Math.random() * analystNames.length)];
  const severity = severities[Math.floor(Math.random() * severities.length)];

  let message = "";
  switch (type) {
    case "alert":
      message = `New ${severity} alert: ${alertNames[Math.floor(Math.random() * alertNames.length)]} from ${sources[Math.floor(Math.random() * sources.length)]}`;
      break;
    case "action":
      message = `${analyst} ${["escalated", "acknowledged", "assigned", "commented on", "began investigating"][Math.floor(Math.random() * 5)]} alert INC-${2026}-${String(Math.floor(Math.random() * 100)).padStart(3, "0")}`;
      break;
    case "status":
      message = `${analyst} changed INC-${2026}-${String(Math.floor(Math.random() * 100)).padStart(3, "0")} status to ${["Investigating", "Containment", "Eradicated", "Resolved"][Math.floor(Math.random() * 4)]}`;
      break;
  }

  return { id: `evt-${id}-${Date.now()}`, timestamp, type, message, severity: type === "alert" ? severity : undefined, analyst };
}
