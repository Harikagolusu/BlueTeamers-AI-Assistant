import { useActivityFeed, type LiveEvent } from "@/hooks/use-realtime-simulation";
import { AlertTriangle, UserCheck, RefreshCw } from "lucide-react";
import { cn } from "@/lib/utils";

const getEventIcon = (type: LiveEvent["type"]) => {
  switch (type) {
    case "alert": return AlertTriangle;
    case "action": return UserCheck;
    case "status": return RefreshCw;
  }
};

const getEventAccent = (event: LiveEvent) => {
  if (event.type === "alert") {
    switch (event.severity) {
      case "Critical": return "text-destructive bg-destructive/10";
      case "High": return "text-orange-400 bg-orange-500/10";
      case "Medium": return "text-yellow-400 bg-yellow-500/10";
      default: return "text-primary bg-primary/10";
    }
  }
  if (event.type === "action") return "text-primary bg-primary/10";
  return "text-secondary bg-secondary/10";
};

const formatTime = (date: Date) => {
  const diff = Math.floor((Date.now() - date.getTime()) / 1000);
  if (diff < 5) return "just now";
  if (diff < 60) return `${diff}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
};

const LiveActivityFeed = () => {
  const events = useActivityFeed(15);

  return (
    <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] shadow-lg shadow-black/20 transition-all duration-300">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.02] via-transparent to-secondary/[0.01] pointer-events-none" />
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

      <div className="relative">
        <div className="px-5 py-4 border-b border-white/[0.06] flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
              <div className="absolute inset-0 w-2 h-2 rounded-full bg-secondary animate-ping opacity-40" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-foreground">Live Activity</h3>
              <p className="text-xs text-muted-foreground mt-0.5">Real-time SOC operations feed</p>
            </div>
          </div>
          <span className="text-[10px] text-muted-foreground px-2 py-1 rounded-full bg-muted/20 border border-white/[0.06]">
            Streaming
          </span>
        </div>

        <div className="max-h-[360px] overflow-y-auto scrollbar-thin">
          {events.map((event, idx) => {
            const Icon = getEventIcon(event.type);
            const accent = getEventAccent(event);
            return (
              <div
                key={event.id}
                className={cn(
                  "flex items-start gap-3 px-5 py-3 border-b border-white/[0.03] last:border-b-0 hover:bg-white/[0.02] transition-all cursor-pointer",
                  idx === 0 && "animate-fade-in"
                )}
              >
                <div className={cn("p-1.5 rounded-md mt-0.5 flex-shrink-0", accent)}>
                  <Icon className="w-3 h-3" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs text-foreground/80 leading-relaxed truncate">{event.message}</p>
                  <span className="text-[10px] text-muted-foreground/60 mt-0.5 block">{formatTime(event.timestamp)}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default LiveActivityFeed;
