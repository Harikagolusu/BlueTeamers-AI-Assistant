import { Shield, Clock, User, ChevronRight, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

const investigations = [
  {
    id: "INC-2026-042",
    title: "Potential Ransomware Activity",
    severity: "Critical",
    assignee: "Sarah M.",
    started: "2h ago",
    alertCount: 8,
    stage: "Containment",
    progress: 65,
  },
  {
    id: "INC-2026-041",
    title: "Lateral Movement Detection",
    severity: "High",
    assignee: "John D.",
    started: "5h ago",
    alertCount: 12,
    stage: "Analysis",
    progress: 40,
  },
  {
    id: "INC-2026-040",
    title: "Credential Harvesting Campaign",
    severity: "High",
    assignee: "Mike R.",
    started: "8h ago",
    alertCount: 5,
    stage: "Eradication",
    progress: 85,
  },
  {
    id: "INC-2026-039",
    title: "Suspicious Outbound C2 Traffic",
    severity: "Medium",
    assignee: "Sarah M.",
    started: "12h ago",
    alertCount: 3,
    stage: "Recovery",
    progress: 92,
  },
];

const getSeverityDot = (severity: string) => {
  switch (severity) {
    case "Critical": return "bg-destructive";
    case "High": return "bg-orange-500";
    case "Medium": return "bg-yellow-500";
    default: return "bg-primary";
  }
};

const getStageColor = (stage: string) => {
  switch (stage) {
    case "Analysis": return "text-primary bg-primary/10 border-primary/20";
    case "Containment": return "text-orange-400 bg-orange-500/10 border-orange-500/20";
    case "Eradication": return "text-yellow-400 bg-yellow-500/10 border-yellow-500/20";
    case "Recovery": return "text-secondary bg-secondary/10 border-secondary/20";
    default: return "text-muted-foreground bg-muted border-border";
  }
};

const ActiveInvestigations = () => {
  return (
    <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 transition-all duration-300">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.02] via-transparent to-secondary/[0.01] pointer-events-none" />
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

      <div className="relative pl-2">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h3 className="text-sm font-semibold text-foreground">Active Investigations</h3>
            <p className="text-xs text-muted-foreground mt-0.5">Ongoing incident response activities</p>
          </div>
          <span className="text-xs text-muted-foreground px-2.5 py-1 rounded-full bg-muted/20 border border-white/[0.06]">
            {investigations.length} active
          </span>
        </div>

        <div className="space-y-3">
          {investigations.map((inv) => (
            <div key={inv.id} className="group/item p-3 rounded-lg hover:bg-white/[0.03] transition-colors cursor-pointer border border-transparent hover:border-white/[0.06]">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-start gap-2.5">
                  <div className={cn("w-2 h-2 rounded-full mt-1.5 flex-shrink-0", getSeverityDot(inv.severity))} />
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono text-muted-foreground">{inv.id}</span>
                      <span className={cn("text-[10px] px-2 py-0.5 rounded-full border font-medium", getStageColor(inv.stage))}>
                        {inv.stage}
                      </span>
                    </div>
                    <h4 className="text-sm font-medium text-foreground mt-0.5 group-hover/item:text-primary transition-colors">{inv.title}</h4>
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-muted-foreground/40 group-hover/item:text-primary transition-colors flex-shrink-0 mt-1" />
              </div>

              <div className="pl-[18px]">
                <div className="flex items-center gap-2 mb-2">
                  <div className="flex-1 h-1.5 bg-muted/30 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-primary to-secondary transition-all"
                      style={{ width: `${inv.progress}%` }}
                    />
                  </div>
                  <span className="text-[10px] text-muted-foreground font-medium">{inv.progress}%</span>
                </div>

                <div className="flex items-center gap-4 text-[10px] text-muted-foreground">
                  <span className="flex items-center gap-1">
                    <User className="w-3 h-3" />{inv.assignee}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />{inv.started}
                  </span>
                  <span className="flex items-center gap-1">
                    <AlertTriangle className="w-3 h-3" />{inv.alertCount} alerts
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ActiveInvestigations;
