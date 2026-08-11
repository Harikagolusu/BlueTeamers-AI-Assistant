import Navbar from "@/components/Navbar";
import SOCSidebar from "@/components/soc/SOCSidebar";
import { Bell, User, Monitor, Shield, Wifi, WifiOff, AlertTriangle, Clock, Cpu, HardDrive, ChevronRight, Search } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface Endpoint {
  id: string;
  hostname: string;
  ip: string;
  os: string;
  osVersion: string;
  status: "Online" | "Offline" | "Isolated";
  risk: "Critical" | "High" | "Medium" | "Low";
  lastSeen: string;
  user: string;
  department: string;
  edrStatus: "Active" | "Outdated" | "Disabled";
  openAlerts: number;
  cpu: number;
  memory: number;
  disk: number;
}

const endpointsData: Endpoint[] = [
  { id: "EP-001", hostname: "WKS-PC-0127", ip: "192.168.1.127", os: "Windows", osVersion: "11 Pro 23H2", status: "Online", risk: "Critical", lastSeen: "Just now", user: "J. Smith", department: "Finance", edrStatus: "Active", openAlerts: 5, cpu: 78, memory: 85, disk: 62 },
  { id: "EP-002", hostname: "WKS-PC-0042", ip: "192.168.1.42", os: "Windows", osVersion: "11 Pro 23H2", status: "Online", risk: "Low", lastSeen: "2m ago", user: "A. Chen", department: "Engineering", edrStatus: "Active", openAlerts: 0, cpu: 45, memory: 52, disk: 38 },
  { id: "EP-003", hostname: "SRV-DB-01", ip: "10.0.0.10", os: "Linux", osVersion: "Ubuntu 22.04 LTS", status: "Online", risk: "Medium", lastSeen: "1m ago", user: "svc_database", department: "IT Infra", edrStatus: "Active", openAlerts: 2, cpu: 92, memory: 88, disk: 75 },
  { id: "EP-004", hostname: "WKS-MKT-015", ip: "192.168.2.15", os: "macOS", osVersion: "Sonoma 14.3", status: "Offline", risk: "High", lastSeen: "3h ago", user: "M. Davis", department: "Marketing", edrStatus: "Outdated", openAlerts: 3, cpu: 0, memory: 0, disk: 91 },
  { id: "EP-005", hostname: "SRV-DEV-02", ip: "10.0.1.22", os: "Linux", osVersion: "CentOS 8 Stream", status: "Isolated", risk: "Critical", lastSeen: "1h ago", user: "svc_deploy", department: "DevOps", edrStatus: "Active", openAlerts: 8, cpu: 34, memory: 67, disk: 55 },
  { id: "EP-006", hostname: "WKS-HR-008", ip: "192.168.3.8", os: "Windows", osVersion: "10 Pro 22H2", status: "Online", risk: "Low", lastSeen: "5m ago", user: "K. Patel", department: "HR", edrStatus: "Active", openAlerts: 0, cpu: 22, memory: 41, disk: 29 },
  { id: "EP-007", hostname: "WKS-EXC-001", ip: "192.168.1.200", os: "Windows", osVersion: "11 Enterprise", status: "Online", risk: "Medium", lastSeen: "Just now", user: "CEO Office", department: "Executive", edrStatus: "Active", openAlerts: 1, cpu: 15, memory: 35, disk: 42 },
  { id: "EP-008", hostname: "SRV-WEB-01", ip: "10.0.2.5", os: "Linux", osVersion: "Debian 12", status: "Online", risk: "Low", lastSeen: "30s ago", user: "svc_nginx", department: "IT Infra", edrStatus: "Active", openAlerts: 0, cpu: 55, memory: 62, disk: 48 },
];

const getRiskStyles = (risk: string) => {
  switch (risk) {
    case "Critical": return "bg-destructive/15 text-destructive border-destructive/25";
    case "High": return "bg-orange-500/15 text-orange-400 border-orange-500/25";
    case "Medium": return "bg-yellow-500/15 text-yellow-400 border-yellow-500/25";
    case "Low": return "bg-primary/15 text-primary border-primary/25";
    default: return "bg-muted text-muted-foreground";
  }
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case "Online": return { icon: Wifi, color: "text-secondary", bg: "bg-secondary/10" };
    case "Offline": return { icon: WifiOff, color: "text-muted-foreground", bg: "bg-muted/20" };
    case "Isolated": return { icon: Shield, color: "text-orange-400", bg: "bg-orange-500/10" };
    default: return { icon: Monitor, color: "text-muted-foreground", bg: "bg-muted/20" };
  }
};

const getEdrStyles = (status: string) => {
  switch (status) {
    case "Active": return "text-secondary";
    case "Outdated": return "text-yellow-400";
    case "Disabled": return "text-destructive";
    default: return "text-muted-foreground";
  }
};

const getBarColor = (value: number) => {
  if (value > 85) return "bg-destructive";
  if (value > 65) return "bg-yellow-500";
  return "bg-primary";
};

const Endpoints = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState("all");

  const filtered = endpointsData.filter(ep => {
    const matchesSearch = ep.hostname.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          ep.ip.includes(searchQuery) ||
                          ep.user.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = filterStatus === "all" || ep.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const counts = {
    online: endpointsData.filter(e => e.status === "Online").length,
    offline: endpointsData.filter(e => e.status === "Offline").length,
    isolated: endpointsData.filter(e => e.status === "Isolated").length,
  };

  return (
    <main className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <SOCSidebar activeItem="Endpoints" />
        <div className="flex-1 flex flex-col min-w-0">
          <header className="bg-card/25 backdrop-blur-lg border-b border-white/[0.08] px-6 py-4 flex items-center justify-between">
            <div>
              <h1 className="text-xl font-semibold text-foreground">Endpoint Inventory</h1>
              <p className="text-sm text-muted-foreground">Monitor and manage all registered endpoints</p>
            </div>
            <div className="flex items-center gap-3">
              <div className="relative hidden md:block">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input type="text" placeholder="Search endpoints..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="bg-background/50 border border-white/[0.08] rounded-lg pl-10 pr-4 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/25 w-64 transition-colors backdrop-blur-sm" />
              </div>
              <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-white/[0.04]"><Bell className="w-5 h-5" /><span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full" /></button>
              <button className="w-8 h-8 bg-primary/10 border border-primary/25 rounded-full flex items-center justify-center text-primary hover:bg-primary/20 transition-colors"><User className="w-4 h-4" /></button>
            </div>
          </header>

          <div className="flex-1 p-6 overflow-auto">
            <div className="space-y-6">
              {/* Stats */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: "Total", count: endpointsData.length, color: "text-foreground", icon: Monitor },
                  { label: "Online", count: counts.online, color: "text-secondary", icon: Wifi },
                  { label: "Offline", count: counts.offline, color: "text-muted-foreground", icon: WifiOff },
                  { label: "Isolated", count: counts.isolated, color: "text-orange-400", icon: Shield },
                ].map((s) => (
                  <div key={s.label} className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-4 shadow-lg shadow-black/20">
                    <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-xs text-muted-foreground uppercase tracking-wide">{s.label}</p>
                        <span className={`text-2xl font-bold ${s.color}`}>{s.count}</span>
                      </div>
                      <s.icon className={`w-5 h-5 ${s.color}`} />
                    </div>
                  </div>
                ))}
              </div>

              {/* Filters */}
              <div className="flex items-center gap-2">
                {["all", "Online", "Offline", "Isolated"].map((status) => (
                  <button key={status} onClick={() => setFilterStatus(status)} className={cn("px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200", filterStatus === status ? "bg-primary/15 text-primary border border-primary/25" : "text-muted-foreground hover:text-foreground hover:bg-white/[0.04] border border-transparent")}>
                    {status === "all" ? "All" : status}
                  </button>
                ))}
                <span className="ml-auto text-xs text-muted-foreground">{filtered.length} endpoints</span>
              </div>

              {/* Endpoint Cards */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {filtered.map((ep) => {
                  const statusInfo = getStatusIcon(ep.status);
                  return (
                    <div key={ep.id} className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 hover:bg-card/35 hover:border-white/[0.12] transition-all duration-300 cursor-pointer">
                      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />

                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center gap-3">
                          <div className={cn("p-2 rounded-lg", statusInfo.bg)}>
                            <Monitor className={cn("w-4 h-4", statusInfo.color)} />
                          </div>
                          <div>
                            <h3 className="text-sm font-semibold text-foreground group-hover:text-primary transition-colors">{ep.hostname}</h3>
                            <span className="text-xs font-mono text-muted-foreground">{ep.ip}</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={cn("text-[10px] px-2 py-0.5 rounded-full border font-medium", getRiskStyles(ep.risk))}>{ep.risk}</span>
                          <ChevronRight className="w-4 h-4 text-muted-foreground/40 group-hover:text-primary transition-colors" />
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-x-4 gap-y-2 mb-3 text-xs">
                        <div className="flex items-center gap-1.5">
                          <span className="text-muted-foreground">OS:</span>
                          <span className="text-foreground">{ep.os} {ep.osVersion}</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <span className="text-muted-foreground">User:</span>
                          <span className="text-foreground">{ep.user}</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <span className="text-muted-foreground">Dept:</span>
                          <span className="text-foreground">{ep.department}</span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <span className="text-muted-foreground">EDR:</span>
                          <span className={getEdrStyles(ep.edrStatus)}>{ep.edrStatus}</span>
                        </div>
                      </div>

                      {ep.status === "Online" && (
                        <div className="space-y-1.5 mb-3">
                          {[
                            { label: "CPU", value: ep.cpu },
                            { label: "MEM", value: ep.memory },
                            { label: "DISK", value: ep.disk },
                          ].map((r) => (
                            <div key={r.label} className="flex items-center gap-2">
                              <span className="text-[9px] text-muted-foreground/60 w-7">{r.label}</span>
                              <div className="flex-1 h-1 bg-muted/20 rounded-full overflow-hidden">
                                <div className={cn("h-full rounded-full transition-all", getBarColor(r.value))} style={{ width: `${r.value}%` }} />
                              </div>
                              <span className="text-[9px] text-muted-foreground/60 w-7 text-right">{r.value}%</span>
                            </div>
                          ))}
                        </div>
                      )}

                      <div className="flex items-center justify-between text-[10px] text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <statusInfo.icon className={cn("w-3 h-3", statusInfo.color)} />
                          <span>{ep.status}</span>
                          <span className="mx-1">·</span>
                          <Clock className="w-3 h-3" />
                          <span>{ep.lastSeen}</span>
                        </div>
                        {ep.openAlerts > 0 && (
                          <span className="flex items-center gap-1 text-destructive">
                            <AlertTriangle className="w-3 h-3" />{ep.openAlerts} alerts
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Endpoints;
