import { useEffect, useState } from "react";
import { CheckCircle2, AlertTriangle, CircleOff, Loader2, Server, BrainCircuit, Database, ShieldCheck } from "lucide-react";

interface HealthData {
  status: string;
  components?: {
    chat_api?: { status?: string };
    rag_engine?: { status?: string; llm?: string };
    memory?: { status?: string; store?: { backend?: string } };
    streaming?: { status?: string };
    cache?: { status?: string };
    guardrails?: { status?: string };
    observability?: { metrics?: string };
  };
}

const REFRESH_MS = 30000;

const HealthStatusIndicator = () => {
  const [health, setHealth] = useState<HealthData | null>(null);
  const [loading, setLoading] = useState(true);
  const [unreachable, setUnreachable] = useState(false);

  useEffect(() => {
    let cancelled = false;
    const poll = async () => {
      try {
        const res = await fetch("/api/health", {
          headers: { Accept: "application/json" },
        });
        if (!res.ok) throw new Error(String(res.status));
        const data = await res.json();
        if (!cancelled) {
          setHealth(data);
          setUnreachable(false);
        }
      } catch {
        if (!cancelled) setUnreachable(true);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    poll();
    const id = setInterval(poll, REFRESH_MS);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, []);

  if (loading) {
    return (
      <div className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg border border-white/[0.08] bg-background/60 backdrop-blur-md text-[10px] font-mono text-muted-foreground">
        <Loader2 className="w-3 h-3 animate-spin text-primary" />
        <span>CHECKING SYSTEM...</span>
      </div>
    );
  }

  const overall = unreachable ? "unreachable" : (health?.status ?? "unknown");
  const color =
    overall === "healthy" ? "text-emerald-400" :
    overall === "degraded" ? "text-yellow-400" :
    overall === "unreachable" ? "text-red-400" : "text-muted-foreground";
  const Icon =
    overall === "healthy" ? CheckCircle2 :
    overall === "degraded" ? AlertTriangle :
    overall === "unreachable" ? CircleOff : Loader2;

  const label =
    overall === "healthy" ? "All Systems Healthy" :
    overall === "degraded" ? "System Degraded" :
    overall === "unreachable" ? "AI Service Unreachable" : "Checking";

  const c = health?.components ?? {};
  const rows: Array<{ icon: typeof Server; name: string; state: string }> = [
    { icon: BrainCircuit, name: "LLM / RAG Engine", state: c.rag_engine?.llm === "healthy" ? "healthy" : c.rag_engine?.status ?? "unknown" },
    { icon: Database, name: "Memory Store", state: c.memory?.status ?? "unknown" },
    { icon: ShieldCheck, name: "Guardrails", state: c.guardrails?.status ?? "unknown" },
    { icon: Server, name: "Chat API", state: c.chat_api?.status ?? "unknown" },
  ];

  return (
    <div className="group relative">
      <div className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg border border-white/[0.08] bg-background/60 backdrop-blur-md text-[10px] font-mono cursor-default transition-all hover:border-white/[0.16]">
        <Icon className={`w-3 h-3 ${color}`} />
        <span className={`${color} uppercase tracking-wider`}>{label}</span>
      </div>

      <div className="absolute bottom-full left-0 mb-2 hidden group-hover:block w-64 rounded-xl border border-white/[0.1] bg-zinc-950/95 backdrop-blur-xl p-3 shadow-2xl z-30">
        <div className="text-[9px] font-mono text-muted-foreground uppercase tracking-widest mb-2">
          AI Service Status
        </div>
        <div className="space-y-1.5">
          {rows.map((r) => (
            <div key={r.name} className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-1.5 text-[10px] text-zinc-300">
                <r.icon className="w-3 h-3 text-muted-foreground" />
                {r.name}
              </span>
              <span
                className={`text-[9px] uppercase font-mono ${
                  r.state === "healthy" || r.state === "disabled"
                    ? "text-emerald-400"
                    : r.state === "degraded"
                    ? "text-yellow-400"
                    : "text-red-400"
                }`}
              >
                {r.state}
              </span>
            </div>
          ))}
        </div>
        <div className="mt-2 pt-2 border-t border-white/[0.06] text-[9px] text-muted-foreground font-mono">
          Refreshes every {REFRESH_MS / 1000}s
        </div>
      </div>
    </div>
  );
};

export default HealthStatusIndicator;
