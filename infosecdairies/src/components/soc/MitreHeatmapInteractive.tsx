import { useState } from "react";
import { cn } from "@/lib/utils";
import { X, Shield } from "lucide-react";

interface Technique {
  id: string;
  name: string;
  detections: number;
  status: "active" | "partial" | "none";
}

interface Tactic {
  name: string;
  id: string;
  count: number;
  techniques: Technique[];
}

const tactics: Tactic[] = [
  { name: "Initial Access", id: "TA0001", count: 8, techniques: [
    { id: "T1566", name: "Phishing", detections: 4, status: "active" },
    { id: "T1190", name: "Exploit Public-Facing App", detections: 2, status: "active" },
    { id: "T1133", name: "External Remote Services", detections: 1, status: "partial" },
    { id: "T1078", name: "Valid Accounts", detections: 1, status: "partial" },
  ]},
  { name: "Execution", id: "TA0002", count: 15, techniques: [
    { id: "T1059.001", name: "PowerShell", detections: 6, status: "active" },
    { id: "T1059.003", name: "Windows Command Shell", detections: 4, status: "active" },
    { id: "T1204", name: "User Execution", detections: 3, status: "active" },
    { id: "T1047", name: "WMI", detections: 2, status: "partial" },
  ]},
  { name: "Persistence", id: "TA0003", count: 12, techniques: [
    { id: "T1543.003", name: "Windows Service", detections: 5, status: "active" },
    { id: "T1053.005", name: "Scheduled Task", detections: 4, status: "active" },
    { id: "T1547.001", name: "Registry Run Keys", detections: 3, status: "partial" },
  ]},
  { name: "Priv. Escalation", id: "TA0004", count: 6, techniques: [
    { id: "T1548.002", name: "UAC Bypass", detections: 3, status: "active" },
    { id: "T1068", name: "Exploitation for Priv Esc", detections: 2, status: "partial" },
    { id: "T1134", name: "Access Token Manipulation", detections: 1, status: "none" },
  ]},
  { name: "Defense Evasion", id: "TA0005", count: 9, techniques: [
    { id: "T1070.004", name: "File Deletion", detections: 3, status: "active" },
    { id: "T1027", name: "Obfuscated Files", detections: 3, status: "active" },
    { id: "T1562.001", name: "Disable Security Tools", detections: 2, status: "partial" },
    { id: "T1036", name: "Masquerading", detections: 1, status: "none" },
  ]},
  { name: "Credential Access", id: "TA0006", count: 18, techniques: [
    { id: "T1110", name: "Brute Force", detections: 8, status: "active" },
    { id: "T1003", name: "OS Credential Dumping", detections: 5, status: "active" },
    { id: "T1558", name: "Kerberoasting", detections: 3, status: "active" },
    { id: "T1552", name: "Unsecured Credentials", detections: 2, status: "partial" },
  ]},
  { name: "Discovery", id: "TA0007", count: 22, techniques: [
    { id: "T1046", name: "Network Service Scanning", detections: 8, status: "active" },
    { id: "T1087", name: "Account Discovery", detections: 6, status: "active" },
    { id: "T1082", name: "System Information", detections: 5, status: "active" },
    { id: "T1018", name: "Remote System Discovery", detections: 3, status: "partial" },
  ]},
  { name: "Lateral Movement", id: "TA0008", count: 4, techniques: [
    { id: "T1021.001", name: "Remote Desktop", detections: 2, status: "active" },
    { id: "T1570", name: "Lateral Tool Transfer", detections: 1, status: "partial" },
    { id: "T1021.002", name: "SMB/Admin Shares", detections: 1, status: "none" },
  ]},
  { name: "Collection", id: "TA0009", count: 7, techniques: [
    { id: "T1560", name: "Archive Collected Data", detections: 3, status: "active" },
    { id: "T1074", name: "Data Staged", detections: 2, status: "partial" },
    { id: "T1005", name: "Data from Local System", detections: 2, status: "none" },
  ]},
  { name: "C&C", id: "TA0011", count: 11, techniques: [
    { id: "T1071.004", name: "DNS", detections: 4, status: "active" },
    { id: "T1071.001", name: "Web Protocols", detections: 4, status: "active" },
    { id: "T1573", name: "Encrypted Channel", detections: 3, status: "partial" },
  ]},
  { name: "Exfiltration", id: "TA0010", count: 5, techniques: [
    { id: "T1041", name: "Exfil Over C2 Channel", detections: 3, status: "active" },
    { id: "T1048", name: "Exfil Over Alt Protocol", detections: 2, status: "partial" },
  ]},
  { name: "Impact", id: "TA0040", count: 3, techniques: [
    { id: "T1486", name: "Data Encrypted for Impact", detections: 2, status: "active" },
    { id: "T1489", name: "Service Stop", detections: 1, status: "partial" },
  ]},
];

const getHeatColor = (count: number) => {
  if (count >= 18) return "bg-destructive/60 border-destructive/40 text-destructive";
  if (count >= 12) return "bg-orange-500/40 border-orange-500/30 text-orange-400";
  if (count >= 8) return "bg-yellow-500/30 border-yellow-500/25 text-yellow-400";
  if (count >= 4) return "bg-primary/25 border-primary/20 text-primary";
  return "bg-muted/20 border-white/[0.06] text-muted-foreground";
};

const getStatusBadge = (status: string) => {
  switch (status) {
    case "active": return "bg-secondary/15 text-secondary border-secondary/25";
    case "partial": return "bg-yellow-500/15 text-yellow-400 border-yellow-500/25";
    default: return "bg-destructive/15 text-destructive border-destructive/25";
  }
};

const MitreHeatmapInteractive = () => {
  const [selectedTactic, setSelectedTactic] = useState<Tactic | null>(null);

  return (
    <div className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 hover:bg-card/35 hover:border-white/[0.12] transition-all duration-300">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

      <div className="relative pl-2">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h3 className="text-sm font-semibold text-foreground">MITRE ATT&CK Coverage</h3>
            <p className="text-xs text-muted-foreground mt-0.5">Click a tactic to view techniques and detections</p>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="text-[9px] text-muted-foreground">Low</span>
            <div className="flex gap-0.5">
              <div className="w-3 h-2 rounded-sm bg-muted/20" />
              <div className="w-3 h-2 rounded-sm bg-primary/25" />
              <div className="w-3 h-2 rounded-sm bg-yellow-500/30" />
              <div className="w-3 h-2 rounded-sm bg-orange-500/40" />
              <div className="w-3 h-2 rounded-sm bg-destructive/60" />
            </div>
            <span className="text-[9px] text-muted-foreground">High</span>
          </div>
        </div>

        <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
          {tactics.map((tactic) => (
            <div
              key={tactic.id}
              onClick={() => setSelectedTactic(selectedTactic?.id === tactic.id ? null : tactic)}
              className={cn(
                "relative p-3 rounded-lg border cursor-pointer hover:scale-105 transition-all duration-200",
                getHeatColor(tactic.count),
                selectedTactic?.id === tactic.id && "ring-2 ring-primary/50 scale-105"
              )}
            >
              <div className="text-center">
                <span className="block text-lg font-bold">{tactic.count}</span>
                <span className="block text-[9px] leading-tight mt-1 opacity-80">{tactic.name}</span>
                <span className="block text-[8px] opacity-50 mt-0.5">{tactic.id}</span>
              </div>
            </div>
          ))}
        </div>

        {selectedTactic && (
          <div className="mt-4 rounded-lg bg-background/60 border border-white/[0.08] overflow-hidden animate-fade-in">
            <div className="px-4 py-3 border-b border-white/[0.06] flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Shield className="w-4 h-4 text-primary" />
                <div>
                  <h4 className="text-sm font-semibold text-foreground">{selectedTactic.name}</h4>
                  <span className="text-[10px] text-muted-foreground font-mono">{selectedTactic.id} • {selectedTactic.techniques.length} techniques mapped</span>
                </div>
              </div>
              <button
                onClick={() => setSelectedTactic(null)}
                className="p-1.5 rounded-md hover:bg-white/[0.06] text-muted-foreground hover:text-foreground transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="divide-y divide-white/[0.04]">
              {selectedTactic.techniques.map((tech) => (
                <div key={tech.id} className="px-4 py-3 flex items-center justify-between hover:bg-white/[0.02] transition-colors">
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono text-primary/70 bg-primary/5 px-1.5 py-0.5 rounded border border-primary/10 flex-shrink-0">
                      {tech.id}
                    </span>
                    <span className="text-sm text-foreground">{tech.name}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-muted-foreground">{tech.detections} detections</span>
                    <span className={cn("text-[10px] px-2 py-0.5 rounded-full border font-medium capitalize", getStatusBadge(tech.status))}>
                      {tech.status === "none" ? "no coverage" : tech.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MitreHeatmapInteractive;
