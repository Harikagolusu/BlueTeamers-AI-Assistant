import { cn } from "@/lib/utils";
import { Monitor, Globe, User, Shield } from "lucide-react";

const alerts = [
  { time: "14:32:18", name: "Suspicious PowerShell Execution", severity: "Critical", source: "WKS-PC-0127", sourceType: "endpoint", status: "Open", mitre: "T1059.001" },
  { time: "14:28:45", name: "Failed Login Attempt (5x)", severity: "High", source: "192.168.1.105", sourceType: "network", status: "Investigating", mitre: "T1110" },
  { time: "14:25:12", name: "Unusual Outbound Traffic", severity: "High", source: "10.0.0.42", sourceType: "network", status: "Open", mitre: "T1041" },
  { time: "14:22:33", name: "New Service Installed", severity: "Medium", source: "SRV-DB-01", sourceType: "server", status: "Resolved", mitre: "T1543.003" },
  { time: "14:18:56", name: "Port Scan Detected", severity: "Medium", source: "172.16.0.88", sourceType: "network", status: "Open", mitre: "T1046" },
  { time: "14:15:21", name: "USB Device Connected", severity: "Low", source: "WKS-PC-0042", sourceType: "endpoint", status: "Resolved", mitre: "T1091" },
  { time: "14:12:09", name: "DNS Query to Suspicious Domain", severity: "High", source: "admin_user", sourceType: "user", status: "Investigating", mitre: "T1071.004" },
  { time: "14:08:44", name: "Scheduled Task Created", severity: "Medium", source: "192.168.1.78", sourceType: "network", status: "Open", mitre: "T1053.005" },
];

const getSeverityStyles = (severity: string) => {
  switch (severity) {
    case "Critical": return "bg-destructive/15 text-destructive border-destructive/25";
    case "High": return "bg-orange-500/15 text-orange-400 border-orange-500/25";
    case "Medium": return "bg-yellow-500/15 text-yellow-400 border-yellow-500/25";
    case "Low": return "bg-primary/15 text-primary border-primary/25";
    default: return "bg-muted text-muted-foreground border-border";
  }
};

const getStatusStyles = (status: string) => {
  switch (status) {
    case "Open": return "text-destructive bg-destructive/10 border-destructive/20";
    case "Investigating": return "text-yellow-400 bg-yellow-500/10 border-yellow-500/20";
    case "Resolved": return "text-secondary bg-secondary/10 border-secondary/20";
    default: return "text-muted-foreground bg-muted border-border";
  }
};

const getSourceIcon = (sourceType: string) => {
  switch (sourceType) {
    case "endpoint": return Monitor;
    case "network": return Globe;
    case "user": return User;
    case "server": return Shield;
    default: return Monitor;
  }
};

const getSeverityBarColor = (severity: string) => {
  switch (severity) {
    case "Critical": return "bg-destructive";
    case "High": return "bg-orange-500";
    case "Medium": return "bg-yellow-500";
    case "Low": return "bg-primary";
    default: return "bg-muted";
  }
};

const RecentAlertsTable = () => {
  return (
    <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] shadow-lg shadow-black/20 transition-all duration-300">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.02] via-transparent to-secondary/[0.01] pointer-events-none" />
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

      <div className="relative">
        <div className="px-5 py-4 border-b border-white/[0.06] flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-foreground">Recent Alerts</h3>
            <p className="text-xs text-muted-foreground mt-0.5">Latest security events requiring attention</p>
          </div>
          <span className="text-xs text-muted-foreground px-2.5 py-1 rounded-full bg-muted/20 border border-white/[0.06]">
            {alerts.length} alerts
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/[0.06]">
                <th className="w-1"></th>
                <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Time</th>
                <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Alert</th>
                <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Severity</th>
                <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Source</th>
                <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">MITRE</th>
                <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((alert, index) => {
                const SourceIcon = getSourceIcon(alert.sourceType);
                return (
                  <tr
                    key={index}
                    className="border-b border-white/[0.03] last:border-b-0 hover:bg-white/[0.03] transition-colors cursor-pointer group"
                  >
                    <td className="w-1 p-0">
                      <div className={cn("w-[3px] h-full min-h-[52px]", getSeverityBarColor(alert.severity))} />
                    </td>
                    <td className="px-4 py-3.5 text-xs text-muted-foreground font-mono">{alert.time}</td>
                    <td className="px-4 py-3.5">
                      <span className="text-sm text-foreground group-hover:text-primary transition-colors">{alert.name}</span>
                    </td>
                    <td className="px-4 py-3.5">
                      <span className={cn(
                        "text-[10px] px-2 py-1 rounded-full border font-medium",
                        getSeverityStyles(alert.severity)
                      )}>
                        {alert.severity}
                      </span>
                    </td>
                    <td className="px-4 py-3.5">
                      <div className="flex items-center gap-1.5">
                        <SourceIcon className="w-3.5 h-3.5 text-muted-foreground" />
                        <span className="text-xs text-muted-foreground font-mono">{alert.source}</span>
                      </div>
                    </td>
                    <td className="px-4 py-3.5">
                      <span className="text-[10px] font-mono text-primary/70 px-1.5 py-0.5 rounded bg-primary/5 border border-primary/10">
                        {alert.mitre}
                      </span>
                    </td>
                    <td className="px-4 py-3.5">
                      <span className={cn("text-[10px] px-2 py-1 rounded-full border font-medium", getStatusStyles(alert.status))}>
                        {alert.status}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default RecentAlertsTable;
