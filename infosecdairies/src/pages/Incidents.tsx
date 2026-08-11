import Navbar from "@/components/Navbar";
import SOCSidebar from "@/components/soc/SOCSidebar";
import { Bell, Search, User, Clock, ChevronRight, AlertTriangle, Shield, Users, CheckCircle, Play } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface Incident {
  id: string;
  title: string;
  severity: "Critical" | "High" | "Medium" | "Low";
  status: "Open" | "Investigating" | "Containment" | "Eradication" | "Recovery" | "Closed";
  assignee: string;
  created: string;
  updated: string;
  alertCount: number;
  affectedAssets: number;
  description: string;
  mitreTactics: string[];
}

const incidentsData: Incident[] = [
  {
    id: "INC-2026-042",
    title: "Potential Ransomware Activity — Finance Dept",
    severity: "Critical",
    status: "Containment",
    assignee: "Sarah M.",
    created: "Feb 11, 2026 06:12",
    updated: "2h ago",
    alertCount: 14,
    affectedAssets: 6,
    description: "Multiple endpoints in the finance department exhibiting encryption behavior. Lateral movement detected from WKS-FIN-003.",
    mitreTactics: ["Execution", "Lateral Movement", "Impact"],
  },
  {
    id: "INC-2026-041",
    title: "Credential Harvesting via Phishing Campaign",
    severity: "High",
    status: "Investigating",
    assignee: "John D.",
    created: "Feb 10, 2026 14:30",
    updated: "5h ago",
    alertCount: 22,
    affectedAssets: 12,
    description: "Phishing emails targeting HR and executive staff. Multiple users submitted credentials to a lookalike domain.",
    mitreTactics: ["Initial Access", "Credential Access"],
  },
  {
    id: "INC-2026-040",
    title: "Suspicious C2 Beaconing from Dev Server",
    severity: "High",
    status: "Eradication",
    assignee: "Mike R.",
    created: "Feb 09, 2026 22:45",
    updated: "8h ago",
    alertCount: 8,
    affectedAssets: 2,
    description: "Periodic beaconing traffic from SRV-DEV-02 to known C2 infrastructure. Cobalt Strike indicators detected.",
    mitreTactics: ["Command and Control", "Persistence"],
  },
  {
    id: "INC-2026-039",
    title: "Unauthorized Service Account Usage",
    severity: "Medium",
    status: "Recovery",
    assignee: "Sarah M.",
    created: "Feb 08, 2026 09:15",
    updated: "12h ago",
    alertCount: 5,
    affectedAssets: 3,
    description: "Service account svc_backup used interactively from unknown workstation. Password rotation initiated.",
    mitreTactics: ["Privilege Escalation", "Defense Evasion"],
  },
  {
    id: "INC-2026-038",
    title: "Port Scan from Internal Host",
    severity: "Low",
    status: "Closed",
    assignee: "John D.",
    created: "Feb 07, 2026 16:00",
    updated: "1d ago",
    alertCount: 3,
    affectedAssets: 1,
    description: "Network scanning activity from IT admin workstation. Confirmed as authorized vulnerability assessment.",
    mitreTactics: ["Discovery"],
  },
  {
    id: "INC-2026-037",
    title: "Data Exfiltration Attempt via Cloud Storage",
    severity: "High",
    status: "Open",
    assignee: "Unassigned",
    created: "Feb 11, 2026 11:30",
    updated: "30m ago",
    alertCount: 6,
    affectedAssets: 1,
    description: "Large file uploads to personal cloud storage detected from marketing department endpoint.",
    mitreTactics: ["Exfiltration", "Collection"],
  },
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
    case "Investigating": return "text-primary bg-primary/10 border-primary/20";
    case "Containment": return "text-orange-400 bg-orange-500/10 border-orange-500/20";
    case "Eradication": return "text-yellow-400 bg-yellow-500/10 border-yellow-500/20";
    case "Recovery": return "text-secondary bg-secondary/10 border-secondary/20";
    case "Closed": return "text-muted-foreground bg-muted/20 border-white/[0.06]";
    default: return "text-muted-foreground bg-muted border-border";
  }
};

const getSeverityDot = (severity: string) => {
  switch (severity) {
    case "Critical": return "bg-destructive";
    case "High": return "bg-orange-500";
    case "Medium": return "bg-yellow-500";
    case "Low": return "bg-primary";
    default: return "bg-muted";
  }
};

const Incidents = () => {
  const [filterStatus, setFilterStatus] = useState("all");

  const filteredIncidents = incidentsData.filter(inc =>
    filterStatus === "all" || inc.status === filterStatus
  );

  const statusCounts = {
    open: incidentsData.filter(i => i.status === "Open").length,
    active: incidentsData.filter(i => ["Investigating", "Containment", "Eradication", "Recovery"].includes(i.status)).length,
    closed: incidentsData.filter(i => i.status === "Closed").length,
  };

  return (
    <main className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <SOCSidebar activeItem="Incidents" />
        <div className="flex-1 flex flex-col min-w-0">
          <header className="bg-card/25 backdrop-blur-lg border-b border-white/[0.08] px-6 py-4 flex items-center justify-between">
            <div>
              <h1 className="text-xl font-semibold text-foreground">Incident Management</h1>
              <p className="text-sm text-muted-foreground">Track and manage security incidents through the IR lifecycle</p>
            </div>
            <div className="flex items-center gap-3">
              <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-white/[0.04]">
                <Bell className="w-5 h-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full" />
              </button>
              <button className="w-8 h-8 bg-primary/10 border border-primary/25 rounded-full flex items-center justify-center text-primary hover:bg-primary/20 transition-colors">
                <User className="w-4 h-4" />
              </button>
            </div>
          </header>

          <div className="flex-1 p-6 overflow-auto">
            <div className="space-y-6">
              {/* Stats */}
              <div className="grid grid-cols-3 gap-4">
                {[
                  { label: "Open", count: statusCounts.open, color: "text-destructive", icon: AlertTriangle, bg: "bg-destructive/10" },
                  { label: "Active", count: statusCounts.active, color: "text-primary", icon: Play, bg: "bg-primary/10" },
                  { label: "Closed", count: statusCounts.closed, color: "text-muted-foreground", icon: CheckCircle, bg: "bg-muted/20" },
                ].map((stat) => (
                  <div key={stat.label} className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20">
                    <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">{stat.label}</p>
                        <span className={`text-3xl font-bold ${stat.color}`}>{stat.count}</span>
                      </div>
                      <div className={`p-2.5 rounded-lg ${stat.bg}`}>
                        <stat.icon className={`w-5 h-5 ${stat.color}`} />
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Filters */}
              <div className="flex items-center gap-2 flex-wrap">
                {["all", "Open", "Investigating", "Containment", "Eradication", "Recovery", "Closed"].map((status) => (
                  <button
                    key={status}
                    onClick={() => setFilterStatus(status)}
                    className={cn(
                      "px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200",
                      filterStatus === status
                        ? "bg-primary/15 text-primary border border-primary/25"
                        : "text-muted-foreground hover:text-foreground hover:bg-white/[0.04] border border-transparent"
                    )}
                  >
                    {status === "all" ? "All" : status}
                  </button>
                ))}
                <span className="ml-auto text-xs text-muted-foreground">
                  {filteredIncidents.length} of {incidentsData.length} incidents
                </span>
              </div>

              {/* Incident Cards */}
              <div className="space-y-3">
                {filteredIncidents.map((incident) => (
                  <div key={incident.id} className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 hover:bg-card/35 hover:border-white/[0.12] transition-all duration-300 cursor-pointer">
                    <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                    <div className="absolute left-0 top-0 bottom-0 w-[3px]">
                      <div className={cn("w-full h-full", getSeverityDot(incident.severity))} />
                    </div>

                    <div className="relative pl-3">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1.5">
                            <span className="text-xs font-mono text-muted-foreground">{incident.id}</span>
                            <span className={cn("text-[10px] px-2 py-0.5 rounded-full border font-medium", getSeverityStyles(incident.severity))}>{incident.severity}</span>
                            <span className={cn("text-[10px] px-2 py-0.5 rounded-full border font-medium", getStatusStyles(incident.status))}>{incident.status}</span>
                          </div>
                          <h3 className="text-sm font-semibold text-foreground group-hover:text-primary transition-colors">{incident.title}</h3>
                        </div>
                        <ChevronRight className="w-4 h-4 text-muted-foreground/40 group-hover:text-primary transition-colors flex-shrink-0 mt-2" />
                      </div>

                      <p className="text-xs text-muted-foreground mb-3 line-clamp-2">{incident.description}</p>

                      <div className="flex flex-wrap gap-1.5 mb-3">
                        {incident.mitreTactics.map((tactic) => (
                          <span key={tactic} className="text-[9px] px-2 py-0.5 rounded bg-primary/5 border border-primary/10 text-primary/70 font-mono">{tactic}</span>
                        ))}
                      </div>

                      <div className="flex items-center gap-4 text-[10px] text-muted-foreground">
                        <span className="flex items-center gap-1"><Users className="w-3 h-3" />{incident.assignee}</span>
                        <span className="flex items-center gap-1"><AlertTriangle className="w-3 h-3" />{incident.alertCount} alerts</span>
                        <span className="flex items-center gap-1"><Shield className="w-3 h-3" />{incident.affectedAssets} assets</span>
                        <span className="flex items-center gap-1"><Clock className="w-3 h-3" />Updated {incident.updated}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Incidents;
