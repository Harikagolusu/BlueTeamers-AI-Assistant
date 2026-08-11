import Navbar from "@/components/Navbar";
import SOCSidebar from "@/components/soc/SOCSidebar";
import { Bell, User, Search, RotateCcw, Download, ChevronDown, ChevronUp, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { queueLogAnalysis } from "@/lib/logAnalysis";

interface LogEntry {
  id: string;
  timestamp: string;
  level: "ERROR" | "WARN" | "INFO" | "DEBUG";
  source: string;
  message: string;
  details?: string;
}

const logsData: LogEntry[] = [
  { id: "L-001", timestamp: "2026-02-11 14:32:18", level: "ERROR", source: "Sysmon", message: "Process creation with encoded PowerShell detected", details: "Process: powershell.exe | PID: 7284 | Parent: WINWORD.EXE | CmdLine: powershell.exe -ep bypass -enc aQBlAHgA..." },
  { id: "L-002", timestamp: "2026-02-11 14:31:55", level: "WARN", source: "Firewall", message: "Outbound connection to known C2 IP blocked", details: "Src: 10.0.0.42:49821 | Dst: 185.220.101.34:443 | Protocol: TCP | Action: BLOCKED" },
  { id: "L-003", timestamp: "2026-02-11 14:30:44", level: "INFO", source: "Windows Auth", message: "Successful user logon", details: "User: jsmith | Domain: CORP | Logon Type: 2 (Interactive) | Workstation: WKS-PC-0127" },
  { id: "L-004", timestamp: "2026-02-11 14:28:12", level: "ERROR", source: "EDR", message: "LSASS memory access from abnormal process", details: "Source: notepad.exe (PID:5544) | Target: lsass.exe | GrantedAccess: 0x1010 | Signature: Mimikatz" },
  { id: "L-005", timestamp: "2026-02-11 14:25:33", level: "WARN", source: "Sysmon", message: "Network connection to suspicious domain", details: "Process: powershell.exe | Remote: update-service-cdn.xyz:443 | Direction: Outbound" },
  { id: "L-006", timestamp: "2026-02-11 14:22:07", level: "INFO", source: "DNS", message: "DNS query resolved", details: "Query: update-service-cdn.xyz | Type: A | Response: 185.220.101.34 | Resolver: 10.0.0.1" },
  { id: "L-007", timestamp: "2026-02-11 14:20:55", level: "ERROR", source: "WAF", message: "Path traversal attempt detected", details: "Src: 45.33.32.156 | Method: POST | URL: /clients/MyCRL | Payload: aCSHELL/../../../etc/shadow | Status: 200" },
  { id: "L-008", timestamp: "2026-02-11 14:18:41", level: "WARN", source: "Windows Auth", message: "Multiple failed login attempts", details: "User: admin_svc | Domain: CORP | Failure Count: 15 | Src IP: 192.168.1.105 | Logon Type: 10 (Remote)" },
  { id: "L-009", timestamp: "2026-02-11 14:15:22", level: "INFO", source: "Firewall", message: "Allowed outbound HTTPS traffic", details: "Src: 10.0.0.5:51200 | Dst: 40.107.22.131:443 | Protocol: TCP | Bytes: 4821" },
  { id: "L-010", timestamp: "2026-02-11 14:12:08", level: "DEBUG", source: "Sysmon", message: "Registry value modification", details: "Path: HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run | Value: WindowsUpdate | Data: C:\\Users\\Public\\update.exe" },
  { id: "L-011", timestamp: "2026-02-11 14:09:34", level: "ERROR", source: "Sysmon", message: "Suspicious file created in temp directory", details: "File: C:\\Users\\jsmith\\AppData\\Local\\Temp\\payload.exe | Hash: a3b9f8c2d1e4f5a6 | Size: 524288 bytes" },
  { id: "L-012", timestamp: "2026-02-11 14:07:19", level: "WARN", source: "Email Gateway", message: "Phishing email quarantined", details: "From: hr-department@company-update.xyz | To: john.smith@corp.local | Subject: Urgent: Verify Your Account | Attachment: verify_account.html" },
  { id: "L-013", timestamp: "2026-02-11 14:05:02", level: "INFO", source: "VPN", message: "VPN connection established", details: "User: mgarcia | Src IP: 203.0.113.50 | Virtual IP: 10.8.0.42 | Protocol: OpenVPN" },
  { id: "L-014", timestamp: "2026-02-11 14:02:47", level: "DEBUG", source: "Windows Auth", message: "Token privilege adjusted", details: "User: SYSTEM | Process: services.exe | Privilege: SeDebugPrivilege | Action: ENABLED" },
  { id: "L-015", timestamp: "2026-02-11 14:00:15", level: "ERROR", source: "IPS", message: "CVE-2024-24919 exploit attempt", details: "Src: 45.33.32.156 | Target: FW-GW-01 | CVE: CVE-2024-24919 | Confidence: HIGH | Action: ALERT" },
];

const levelConfig = {
  ERROR: { color: "text-red-400", bg: "bg-red-500/10", border: "border-red-500/20" },
  WARN: { color: "text-yellow-400", bg: "bg-yellow-500/10", border: "border-yellow-500/20" },
  INFO: { color: "text-primary", bg: "bg-primary/10", border: "border-primary/20" },
  DEBUG: { color: "text-muted-foreground", bg: "bg-muted/10", border: "border-white/[0.06]" },
};

const LabsLogs = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [levelFilter, setLevelFilter] = useState("all");
  const [sourceFilter, setSourceFilter] = useState("all");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const navigate = useNavigate();

  const sources = ["all", ...Array.from(new Set(logsData.map(l => l.source)))];

  const filtered = logsData.filter(l => {
    if (levelFilter !== "all" && l.level !== levelFilter) return false;
    if (sourceFilter !== "all" && l.source !== sourceFilter) return false;
    if (searchQuery && ![l.message, l.source, l.id].some(f => f.toLowerCase().includes(searchQuery.toLowerCase()))) return false;
    return true;
  });

  const analyzeWithAI = () => {
    const logText = logsData
      .map(l => `[${l.timestamp}] ${l.level} ${l.source}: ${l.message}${l.details ? ` | ${l.details}` : ""}`)
      .join("\n");
    queueLogAnalysis("Analyze these security logs and summarize the threats and IOCs.", [
      { name: "security-logs.log", type: "text/plain", content: logText },
    ]);
    navigate("/chat");
  };

  return (
    <main className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <SOCSidebar activeItem="Logs" />
        <div className="flex-1 flex flex-col min-w-0">
          <header className="bg-card/25 backdrop-blur-lg border-b border-white/[0.08] px-6 py-4 flex items-center justify-between">
            <div>
              <h1 className="text-xl font-semibold text-foreground">Log Explorer</h1>
              <p className="text-sm text-muted-foreground">Search and analyze raw security logs</p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={analyzeWithAI}
                className="flex items-center gap-2 px-3 py-2 text-xs font-medium text-primary bg-primary/10 border border-primary/25 rounded-lg hover:bg-primary/20 transition-colors"
                title="Send these logs to the AI assistant for analysis"
              >
                <Sparkles className="w-3.5 h-3.5" />
                Analyze with AI
              </button>
              <button className="p-2 text-muted-foreground hover:text-primary transition-colors rounded-lg hover:bg-white/[0.04]" title="Export">
                <Download className="w-4 h-4" />
              </button>
              <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-white/[0.04]"><Bell className="w-5 h-5" /><span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full" /></button>
              <button className="w-8 h-8 bg-primary/10 border border-primary/25 rounded-full flex items-center justify-center text-primary hover:bg-primary/20 transition-colors"><User className="w-4 h-4" /></button>
            </div>
          </header>

          <div className="flex-1 p-6 overflow-auto">
            <div className="space-y-4">
              {/* Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {(["ERROR", "WARN", "INFO", "DEBUG"] as const).map((level) => {
                  const count = logsData.filter(l => l.level === level).length;
                  const cfg = levelConfig[level];
                  return (
                    <div key={level} onClick={() => setLevelFilter(levelFilter === level ? "all" : level)} className={cn("relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-4 cursor-pointer hover:bg-card/35 transition-all", levelFilter === level && "border-primary/30")}>
                      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                      <p className="text-xs text-muted-foreground uppercase tracking-wide">{level}</p>
                      <span className={cn("text-2xl font-bold", cfg.color)}>{count}</span>
                    </div>
                  );
                })}
              </div>

              {/* Filters */}
              <div className="flex flex-wrap items-center gap-3">
                <div className="relative min-w-[240px]">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <input
                    type="text"
                    placeholder="Search logs..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full bg-card/50 border border-white/[0.08] rounded-lg pl-10 pr-4 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
                  />
                </div>
                <select
                  value={sourceFilter}
                  onChange={(e) => setSourceFilter(e.target.value)}
                  className="bg-card/50 border border-white/[0.08] rounded-lg px-3 py-2 text-sm text-muted-foreground focus:outline-none focus:border-primary/50 cursor-pointer"
                >
                  {sources.map(s => <option key={s} value={s}>{s === "all" ? "All Sources" : s}</option>)}
                </select>
                <button
                  onClick={() => { setSearchQuery(""); setLevelFilter("all"); setSourceFilter("all"); }}
                  className="flex items-center gap-2 px-3 py-2 text-sm text-muted-foreground bg-card/50 border border-white/[0.08] rounded-lg hover:text-foreground hover:border-primary/30 transition-colors"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  Reset
                </button>
                <span className="ml-auto text-xs text-muted-foreground"><span className="text-foreground font-medium">{filtered.length}</span> entries</span>
              </div>

              {/* Log Table */}
              <div className="bg-card/25 border border-white/[0.08] rounded-xl overflow-hidden font-mono text-xs">
                <div className="grid grid-cols-[140px_60px_120px_1fr_40px] border-b border-white/[0.08] px-4 py-2">
                  <span className="text-[10px] text-muted-foreground uppercase tracking-wider">Timestamp</span>
                  <span className="text-[10px] text-muted-foreground uppercase tracking-wider">Level</span>
                  <span className="text-[10px] text-muted-foreground uppercase tracking-wider">Source</span>
                  <span className="text-[10px] text-muted-foreground uppercase tracking-wider">Message</span>
                  <span></span>
                </div>

                {filtered.map((log) => {
                  const cfg = levelConfig[log.level];
                  const isExpanded = expandedId === log.id;
                  return (
                    <div key={log.id}>
                      <div
                        onClick={() => log.details && setExpandedId(isExpanded ? null : log.id)}
                        className={cn("grid grid-cols-[140px_60px_120px_1fr_40px] px-4 py-2.5 border-b border-white/[0.04] transition-colors", log.details && "cursor-pointer", isExpanded ? "bg-primary/5" : log.details ? "hover:bg-white/[0.02]" : "")}
                      >
                        <span className="text-muted-foreground/70 text-[10px] self-center">{log.timestamp}</span>
                        <span className={cn("text-[10px] font-bold self-center", cfg.color)}>{log.level}</span>
                        <span className="text-primary/70 self-center truncate pr-2">{log.source}</span>
                        <span className="text-foreground/80 self-center truncate">{log.message}</span>
                        <div className="flex items-center justify-center">
                          {log.details && (isExpanded ? <ChevronUp className="w-3.5 h-3.5 text-muted-foreground" /> : <ChevronDown className="w-3.5 h-3.5 text-muted-foreground/40" />)}
                        </div>
                      </div>
                      {isExpanded && log.details && (
                        <div className="px-4 py-3 bg-background/50 border-b border-white/[0.04]">
                          <pre className="text-[10px] text-muted-foreground whitespace-pre-wrap break-all leading-relaxed">{log.details}</pre>
                        </div>
                      )}
                    </div>
                  );
                })}

                {filtered.length === 0 && (
                  <div className="text-center py-12 text-muted-foreground text-sm font-sans">No log entries match the current filters.</div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default LabsLogs;
