import { AlertTriangle, AlertCircle, AlertOctagon, Info, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { useRealtimeSimulation, useAnimatedValue, randomVariation } from "@/hooks/use-realtime-simulation";
import { useMemo } from "react";

const baseAlertData = [
  { label: "Total Alerts", baseCount: 1247, icon: AlertOctagon, color: "text-foreground", accentColor: "text-primary", baseTrend: 12, trendDir: "up" as const, subtitle: "Last 24 hours" },
  { label: "Critical", baseCount: 12, icon: AlertOctagon, color: "text-destructive", accentColor: "text-destructive", baseTrend: 3, trendDir: "up" as const, subtitle: "Needs attention" },
  { label: "High", baseCount: 47, icon: AlertCircle, color: "text-orange-400", accentColor: "text-orange-400", baseTrend: -5, trendDir: "down" as const, subtitle: "Under review" },
  { label: "Medium", baseCount: 156, icon: AlertTriangle, color: "text-yellow-400", accentColor: "text-yellow-400", baseTrend: 0, trendDir: "neutral" as const, subtitle: "Monitoring" },
  { label: "Low", baseCount: 1032, icon: Info, color: "text-primary", accentColor: "text-primary", baseTrend: 8, trendDir: "up" as const, subtitle: "Informational" },
];

const getTrendIcon = (dir: "up" | "down" | "neutral") => {
  switch (dir) {
    case "up": return TrendingUp;
    case "down": return TrendingDown;
    case "neutral": return Minus;
  }
};

const getTrendColor = (dir: "up" | "down" | "neutral", label: string) => {
  if (label === "Total Alerts" || label === "Low") {
    return dir === "up" ? "text-muted-foreground" : "text-secondary";
  }
  return dir === "up" ? "text-destructive" : dir === "down" ? "text-secondary" : "text-muted-foreground";
};

const AnimatedCount = ({ value }: { value: number }) => {
  const animated = useAnimatedValue(value);
  return <>{animated.toLocaleString()}</>;
};

const AlertSummaryCards = () => {
  const tick = useRealtimeSimulation(8000);

  const alertData = useMemo(() => {
    return baseAlertData.map((alert) => ({
      ...alert,
      count: randomVariation(alert.baseCount, 5),
      trend: alert.baseTrend === 0 ? "0" : alert.baseTrend > 0 ? `+${randomVariation(alert.baseTrend, 30)}` : `${randomVariation(alert.baseTrend, 30)}`,
    }));
  }, [tick]);

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {alertData.map((alert) => {
        const base = baseAlertData.find((b) => b.label === alert.label)!;
        const TrendIcon = getTrendIcon(base.trendDir);
        const trendColor = getTrendColor(base.trendDir, alert.label);

        return (
          <div
            key={alert.label}
            className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 hover:bg-card/35 hover:border-white/[0.12] hover:translate-y-[-2px] transition-all duration-300 cursor-pointer"
          >
            <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
            <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.02] via-transparent to-secondary/[0.01] pointer-events-none" />
            <div className={`absolute inset-x-0 top-0 h-[2px] opacity-60 ${
              alert.label === "Critical" ? "bg-destructive" :
              alert.label === "High" ? "bg-orange-500" :
              alert.label === "Medium" ? "bg-yellow-500" :
              alert.label === "Low" ? "bg-primary" :
              "bg-gradient-to-r from-primary to-secondary"
            }`} />

            <div className="relative">
              <div className="flex items-center justify-between mb-3">
                <div className={`p-2 rounded-lg ${
                  alert.label === "Critical" ? "bg-destructive/10" :
                  alert.label === "High" ? "bg-orange-500/10" :
                  alert.label === "Medium" ? "bg-yellow-500/10" :
                  alert.label === "Low" ? "bg-primary/10" :
                  "bg-muted/30"
                }`}>
                  <base.icon className={`w-4 h-4 ${base.color}`} />
                </div>
                <div className={`flex items-center gap-1 text-xs ${trendColor}`}>
                  <TrendIcon className="w-3 h-3" />
                  <span>{alert.trend}</span>
                </div>
              </div>

              <div className="mb-1">
                <span className={`text-2xl font-bold ${base.color} group-hover:scale-105 inline-block transition-transform origin-left`}>
                  <AnimatedCount value={alert.count} />
                </span>
              </div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">{alert.label}</p>
              <p className="text-[10px] text-muted-foreground/60 mt-1">{base.subtitle}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default AlertSummaryCards;
