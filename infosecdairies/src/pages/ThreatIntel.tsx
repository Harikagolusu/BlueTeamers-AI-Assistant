import Navbar from "@/components/Navbar";
import SOCSidebar from "@/components/soc/SOCSidebar";
import { Bell, User, Globe, Shield, FileText, ExternalLink, AlertTriangle, Clock, Search, Hash, Crosshair, Eye } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface IOC {
  id: string;
  type: "IP" | "Domain" | "Hash" | "URL" | "Email";
  value: string;
  threat: string;
  confidence: "High" | "Medium" | "Low";
  source: string;
  firstSeen: string;
  lastSeen: string;
  tags: string[];
}

interface ThreatActor {
  name: string;
  aliases: string[];
  origin: string;
  motivation: string;
  targetSectors: string[];
  activeSince: string;
  confidence: "High" | "Medium" | "Low";
  associatedMalware: string[];
  ttps: string[];
  lastActivity: string;
}

const iocData: IOC[] = [
  { id: "IOC-001", type: "IP", value: "185.220.101.34", threat: "C2 Server — Cobalt Strike", confidence: "High", source: "AlienVault OTX", firstSeen: "Feb 08", lastSeen: "Feb 11", tags: ["APT", "C2", "Cobalt Strike"] },
  { id: "IOC-002", type: "Domain", value: "update-service-cdn.xyz", threat: "Phishing Infrastructure", confidence: "High", source: "PhishTank", firstSeen: "Feb 09", lastSeen: "Feb 11", tags: ["Phishing", "Credential Theft"] },
  { id: "IOC-003", type: "Hash", value: "a3b9f...8c2d1 (SHA256)", threat: "Emotet Dropper", confidence: "Medium", source: "MalwareBazaar", firstSeen: "Feb 10", lastSeen: "Feb 10", tags: ["Emotet", "Dropper", "Macro"] },
  { id: "IOC-004", type: "URL", value: "hxxps://login-verify[.]net/auth", threat: "Credential Harvester", confidence: "High", source: "Internal Hunt", firstSeen: "Feb 11", lastSeen: "Feb 11", tags: ["Phishing", "OAuth Abuse"] },
  { id: "IOC-005", type: "IP", value: "91.234.99.117", threat: "Scanning/Reconnaissance", confidence: "Low", source: "AbuseIPDB", firstSeen: "Feb 06", lastSeen: "Feb 11", tags: ["Scanner", "Brute Force"] },
  { id: "IOC-006", type: "Email", value: "ceo-office@company-hr[.]com", threat: "BEC Impersonation", confidence: "Medium", source: "Internal Report", firstSeen: "Feb 10", lastSeen: "Feb 11", tags: ["BEC", "Social Engineering"] },
  { id: "IOC-007", type: "Hash", value: "7f8e2...4a91b (MD5)", threat: "Qakbot Payload", confidence: "High", source: "VirusTotal", firstSeen: "Feb 07", lastSeen: "Feb 09", tags: ["Qakbot", "Banking Trojan"] },
  { id: "IOC-008", type: "Domain", value: "cdn-analytics-track[.]com", threat: "Magecart Skimmer", confidence: "Medium", source: "URLhaus", firstSeen: "Feb 05", lastSeen: "Feb 10", tags: ["Web Skimmer", "PCI"] },
];

const threatActors: ThreatActor[] = [
  {
    name: "VELVET TEMPEST",
    aliases: ["APT-VT", "SilkStorm"],
    origin: "Eastern Europe",
    motivation: "Financial Gain",
    targetSectors: ["Finance", "Healthcare", "Retail"],
    activeSince: "2021",
    confidence: "High",
    associatedMalware: ["Cobalt Strike", "Emotet", "TrickBot"],
    ttps: ["T1566", "T1059.001", "T1071.001", "T1486"],
    lastActivity: "Feb 11, 2026",
  },
  {
    name: "PHANTOM CRANE",
    aliases: ["GhostOps"],
    origin: "Southeast Asia",
    motivation: "Espionage",
    targetSectors: ["Government", "Defense", "Energy"],
    activeSince: "2019",
    confidence: "Medium",
    associatedMalware: ["ShadowPad", "PlugX"],
    ttps: ["T1190", "T1505.003", "T1003.001"],
    lastActivity: "Feb 09, 2026",
  },
  {
    name: "NEON SPIDER",
    aliases: ["CryptoWeb", "NS-Group"],
    origin: "Unknown",
    motivation: "Ransomware Operations",
    targetSectors: ["Manufacturing", "Legal", "Education"],
    activeSince: "2023",
    confidence: "High",
    associatedMalware: ["BlackCat", "SystemBC"],
    ttps: ["T1486", "T1490", "T1021.001", "T1078"],
    lastActivity: "Feb 10, 2026",
  },
];

const getConfidenceStyles = (c: string) => {
  switch (c) {
    case "High": return "bg-destructive/15 text-destructive border-destructive/25";
    case "Medium": return "bg-yellow-500/15 text-yellow-400 border-yellow-500/25";
    case "Low": return "bg-muted/20 text-muted-foreground border-white/[0.06]";
    default: return "bg-muted text-muted-foreground";
  }
};

const getTypeIcon = (type: string) => {
  switch (type) {
    case "IP": return Globe;
    case "Domain": return Globe;
    case "Hash": return Hash;
    case "URL": return ExternalLink;
    case "Email": return FileText;
    default: return Shield;
  }
};

const ThreatIntel = () => {
  const [activeTab, setActiveTab] = useState<"iocs" | "actors">("iocs");
  const [searchQuery, setSearchQuery] = useState("");

  const filteredIOCs = iocData.filter(ioc =>
    ioc.value.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ioc.threat.toLowerCase().includes(searchQuery.toLowerCase()) ||
    ioc.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <main className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <SOCSidebar activeItem="Threat Intel" />
        <div className="flex-1 flex flex-col min-w-0">
          <header className="bg-card/25 backdrop-blur-lg border-b border-white/[0.08] px-6 py-4 flex items-center justify-between">
            <div>
              <h1 className="text-xl font-semibold text-foreground">Threat Intelligence</h1>
              <p className="text-sm text-muted-foreground">IOC management and threat actor tracking</p>
            </div>
            <div className="flex items-center gap-3">
              <div className="relative hidden md:block">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input type="text" placeholder="Search IOCs, actors..." value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="bg-background/50 border border-white/[0.08] rounded-lg pl-10 pr-4 py-2 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/25 w-64 transition-colors backdrop-blur-sm" />
              </div>
              <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-white/[0.04]"><Bell className="w-5 h-5" /><span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full" /></button>
              <button className="w-8 h-8 bg-primary/10 border border-primary/25 rounded-full flex items-center justify-center text-primary hover:bg-primary/20 transition-colors"><User className="w-4 h-4" /></button>
            </div>
          </header>

          <div className="flex-1 p-6 overflow-auto">
            <div className="space-y-6">
              {/* Tabs */}
              <div className="flex items-center gap-2">
                <button onClick={() => setActiveTab("iocs")} className={cn("px-4 py-2 rounded-lg text-sm font-medium transition-all", activeTab === "iocs" ? "bg-primary/15 text-primary border border-primary/25" : "text-muted-foreground hover:text-foreground hover:bg-white/[0.04]")}>
                  <span className="flex items-center gap-2"><Crosshair className="w-4 h-4" />Indicators of Compromise</span>
                </button>
                <button onClick={() => setActiveTab("actors")} className={cn("px-4 py-2 rounded-lg text-sm font-medium transition-all", activeTab === "actors" ? "bg-primary/15 text-primary border border-primary/25" : "text-muted-foreground hover:text-foreground hover:bg-white/[0.04]")}>
                  <span className="flex items-center gap-2"><Eye className="w-4 h-4" />Threat Actors</span>
                </button>
              </div>

              {/* IOCs Tab */}
              {activeTab === "iocs" && (
                <>
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    {[
                      { label: "Total IOCs", count: iocData.length, color: "text-foreground" },
                      { label: "IPs", count: iocData.filter(i => i.type === "IP").length, color: "text-primary" },
                      { label: "Domains", count: iocData.filter(i => i.type === "Domain").length, color: "text-secondary" },
                      { label: "Hashes", count: iocData.filter(i => i.type === "Hash").length, color: "text-yellow-400" },
                      { label: "High Conf.", count: iocData.filter(i => i.confidence === "High").length, color: "text-destructive" },
                    ].map((s) => (
                      <div key={s.label} className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-4 shadow-lg shadow-black/20">
                        <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                        <p className="text-xs text-muted-foreground uppercase tracking-wide">{s.label}</p>
                        <span className={`text-2xl font-bold ${s.color}`}>{s.count}</span>
                      </div>
                    ))}
                  </div>

                  <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] shadow-lg shadow-black/20">
                    <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead>
                          <tr className="border-b border-white/[0.06]">
                            <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Type</th>
                            <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Value</th>
                            <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Threat</th>
                            <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Confidence</th>
                            <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Source</th>
                            <th className="text-left text-[10px] font-medium text-muted-foreground uppercase tracking-wider px-4 py-3">Tags</th>
                          </tr>
                        </thead>
                        <tbody>
                          {filteredIOCs.map((ioc) => {
                            const TypeIcon = getTypeIcon(ioc.type);
                            return (
                              <tr key={ioc.id} className="border-b border-white/[0.03] last:border-b-0 hover:bg-white/[0.03] transition-colors cursor-pointer group">
                                <td className="px-4 py-3">
                                  <div className="flex items-center gap-1.5">
                                    <TypeIcon className="w-3.5 h-3.5 text-primary" />
                                    <span className="text-xs text-muted-foreground">{ioc.type}</span>
                                  </div>
                                </td>
                                <td className="px-4 py-3"><span className="text-xs font-mono text-foreground group-hover:text-primary transition-colors">{ioc.value}</span></td>
                                <td className="px-4 py-3"><span className="text-xs text-foreground">{ioc.threat}</span></td>
                                <td className="px-4 py-3"><span className={cn("text-[10px] px-2 py-0.5 rounded-full border font-medium", getConfidenceStyles(ioc.confidence))}>{ioc.confidence}</span></td>
                                <td className="px-4 py-3"><span className="text-xs text-muted-foreground">{ioc.source}</span></td>
                                <td className="px-4 py-3">
                                  <div className="flex flex-wrap gap-1">
                                    {ioc.tags.map((tag) => (
                                      <span key={tag} className="text-[9px] px-1.5 py-0.5 rounded bg-primary/5 border border-primary/10 text-primary/70">{tag}</span>
                                    ))}
                                  </div>
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </>
              )}

              {/* Threat Actors Tab */}
              {activeTab === "actors" && (
                <div className="space-y-4">
                  {threatActors.map((actor) => (
                    <div key={actor.name} className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 hover:bg-card/35 hover:border-white/[0.12] transition-all duration-300">
                      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

                      <div className="relative pl-3">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <div className="flex items-center gap-2 mb-1">
                              <h3 className="text-base font-bold text-foreground group-hover:text-primary transition-colors">{actor.name}</h3>
                              <span className={cn("text-[10px] px-2 py-0.5 rounded-full border font-medium", getConfidenceStyles(actor.confidence))}>{actor.confidence} Confidence</span>
                            </div>
                            <div className="flex items-center gap-3 text-xs text-muted-foreground">
                              <span>AKA: {actor.aliases.join(", ")}</span>
                              <span>·</span>
                              <span>{actor.origin}</span>
                              <span>·</span>
                              <span>Active since {actor.activeSince}</span>
                            </div>
                          </div>
                          <span className="text-[10px] text-muted-foreground flex items-center gap-1"><Clock className="w-3 h-3" />Last: {actor.lastActivity}</span>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-3">
                          <div>
                            <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-1.5">Motivation</p>
                            <span className="text-xs text-foreground px-2 py-1 rounded bg-primary/5 border border-primary/10">{actor.motivation}</span>
                          </div>
                          <div>
                            <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-1.5">Target Sectors</p>
                            <div className="flex flex-wrap gap-1">{actor.targetSectors.map(s => <span key={s} className="text-[10px] px-1.5 py-0.5 rounded bg-orange-500/5 border border-orange-500/10 text-orange-400/80">{s}</span>)}</div>
                          </div>
                          <div>
                            <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-1.5">Malware</p>
                            <div className="flex flex-wrap gap-1">{actor.associatedMalware.map(m => <span key={m} className="text-[10px] px-1.5 py-0.5 rounded bg-destructive/5 border border-destructive/10 text-destructive/80">{m}</span>)}</div>
                          </div>
                        </div>

                        <div>
                          <p className="text-[10px] text-muted-foreground uppercase tracking-wide mb-1.5">MITRE ATT&CK TTPs</p>
                          <div className="flex flex-wrap gap-1">{actor.ttps.map(t => <span key={t} className="text-[9px] px-1.5 py-0.5 rounded bg-primary/5 border border-primary/10 text-primary/70 font-mono">{t}</span>)}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default ThreatIntel;
