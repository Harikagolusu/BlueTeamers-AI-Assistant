import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

interface ThreatSource {
  id: string;
  country: string;
  code: string;
  lat: number;
  lng: number;
  attacks: number;
  severity: "Critical" | "High" | "Medium" | "Low";
  type: string;
}

const threatSources: ThreatSource[] = [
  { id: "1", country: "Russia", code: "RU", lat: 55.7, lng: 37.6, attacks: 342, severity: "Critical", type: "APT Activity" },
  { id: "2", country: "China", code: "CN", lat: 39.9, lng: 116.4, attacks: 287, severity: "Critical", type: "Espionage" },
  { id: "3", country: "North Korea", code: "KP", lat: 39.0, lng: 125.7, attacks: 156, severity: "High", type: "Ransomware" },
  { id: "4", country: "Iran", code: "IR", lat: 35.7, lng: 51.4, attacks: 128, severity: "High", type: "Wipers" },
  { id: "5", country: "Brazil", code: "BR", lat: -15.8, lng: -47.9, attacks: 95, severity: "Medium", type: "Credential Theft" },
  { id: "6", country: "Nigeria", code: "NG", lat: 9.1, lng: 7.5, attacks: 78, severity: "Medium", type: "BEC/Phishing" },
  { id: "7", country: "India", code: "IN", lat: 28.6, lng: 77.2, attacks: 64, severity: "Low", type: "Port Scanning" },
  { id: "8", country: "Romania", code: "RO", lat: 44.4, lng: 26.1, attacks: 53, severity: "Medium", type: "Botnet C2" },
];

const getSeverityColor = (severity: string) => {
  switch (severity) {
    case "Critical": return { dot: "bg-destructive", ring: "ring-destructive/30", text: "text-destructive" };
    case "High": return { dot: "bg-orange-500", ring: "ring-orange-500/30", text: "text-orange-400" };
    case "Medium": return { dot: "bg-yellow-500", ring: "ring-yellow-500/30", text: "text-yellow-400" };
    default: return { dot: "bg-primary", ring: "ring-primary/30", text: "text-primary" };
  }
};

const toPosition = (lat: number, lng: number) => ({
  x: ((lng + 180) / 360) * 100,
  y: ((90 - lat) / 180) * 100,
});

const ThreatGeoMap = () => {
  const [activeSource, setActiveSource] = useState<string | null>(null);
  const [, setPulsePhase] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setPulsePhase((p) => p + 1), 2000);
    return () => clearInterval(id);
  }, []);

  const target = toPosition(38.9, -77.0);

  return (
    <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 transition-all duration-300">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

      <div className="relative pl-2">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-semibold text-foreground">Threat Origins</h3>
            <p className="text-xs text-muted-foreground mt-0.5">Global attack source distribution</p>
          </div>
          <div className="flex items-center gap-3">
            {["Critical", "High", "Medium", "Low"].map((s) => {
              const c = getSeverityColor(s);
              return (
                <div key={s} className="flex items-center gap-1.5">
                  <div className={cn("w-2 h-2 rounded-full", c.dot)} />
                  <span className="text-[9px] text-muted-foreground">{s}</span>
                </div>
              );
            })}
          </div>
        </div>

        <div className="relative w-full aspect-[2/1] bg-background/40 rounded-lg border border-white/[0.06] overflow-hidden">
          <div className="absolute inset-0 circuit-pattern opacity-30" />

          <div className="absolute inset-0 opacity-[0.06]"
            style={{
              background: `
                radial-gradient(ellipse 18% 12% at 25% 38%, hsl(186 100% 42%) 0%, transparent 100%),
                radial-gradient(ellipse 8% 16% at 50% 30%, hsl(186 100% 42%) 0%, transparent 100%),
                radial-gradient(ellipse 12% 10% at 53% 42%, hsl(186 100% 42%) 0%, transparent 100%),
                radial-gradient(ellipse 20% 14% at 72% 40%, hsl(186 100% 42%) 0%, transparent 100%),
                radial-gradient(ellipse 6% 14% at 42% 60%, hsl(186 100% 42%) 0%, transparent 100%),
                radial-gradient(ellipse 8% 8% at 80% 70%, hsl(186 100% 42%) 0%, transparent 100%)
              `
            }}
          />

          <div
            className="absolute z-20"
            style={{ left: `${target.x}%`, top: `${target.y}%`, transform: "translate(-50%, -50%)" }}
          >
            <div className="w-3 h-3 rounded-full bg-secondary ring-4 ring-secondary/20" />
          </div>

          {threatSources.map((source) => {
            const pos = toPosition(source.lat, source.lng);
            const colors = getSeverityColor(source.severity);
            const isActive = activeSource === source.id;

            return (
              <div key={source.id}>
                <svg className="absolute inset-0 w-full h-full pointer-events-none z-10" style={{ opacity: 0.3 }}>
                  <line
                    x1={`${pos.x}%`} y1={`${pos.y}%`}
                    x2={`${target.x}%`} y2={`${target.y}%`}
                    stroke={source.severity === "Critical" ? "hsl(0 84% 60%)" : source.severity === "High" ? "hsl(25 95% 53%)" : "hsl(186 100% 42%)"}
                    strokeWidth="0.5"
                    strokeDasharray="4 4"
                    className="animate-pulse"
                  />
                </svg>

                <div
                  className="absolute z-20 cursor-pointer group/dot"
                  style={{ left: `${pos.x}%`, top: `${pos.y}%`, transform: "translate(-50%, -50%)" }}
                  onMouseEnter={() => setActiveSource(source.id)}
                  onMouseLeave={() => setActiveSource(null)}
                >
                  <div className={cn("w-2.5 h-2.5 rounded-full ring-2 transition-all", colors.dot, colors.ring, isActive && "scale-150")} />

                  {isActive && (
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 bg-card/95 backdrop-blur-lg border border-white/[0.12] rounded-lg shadow-xl z-30 whitespace-nowrap animate-fade-in">
                      <div className="flex items-center gap-2 mb-1">
                        <span className={cn("text-xs font-semibold", colors.text)}>{source.country}</span>
                        <span className="text-[10px] text-muted-foreground font-mono">{source.code}</span>
                      </div>
                      <div className="text-[10px] text-muted-foreground">{source.type}</div>
                      <div className="text-xs text-foreground font-bold mt-1">{source.attacks} attacks</div>
                      <div className="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-white/[0.12]" />
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-2">
          {threatSources.slice(0, 4).map((source) => {
            const colors = getSeverityColor(source.severity);
            return (
              <div
                key={source.id}
                className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/[0.02] border border-white/[0.06] hover:bg-white/[0.04] transition-colors cursor-pointer"
                onMouseEnter={() => setActiveSource(source.id)}
                onMouseLeave={() => setActiveSource(null)}
              >
                <div className={cn("w-2 h-2 rounded-full flex-shrink-0", colors.dot)} />
                <div className="min-w-0">
                  <span className="text-[10px] text-foreground font-medium block truncate">{source.country}</span>
                  <span className="text-[9px] text-muted-foreground">{source.attacks} attacks</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ThreatGeoMap;
