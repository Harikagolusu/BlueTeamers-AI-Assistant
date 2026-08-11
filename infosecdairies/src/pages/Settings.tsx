import Navbar from "@/components/Navbar";
import SOCSidebar from "@/components/soc/SOCSidebar";
import { Bell, User, Settings as SettingsIcon, Shield, Mail, Smartphone, Clock, Database, Globe, Zap, AlertTriangle, Users, Monitor } from "lucide-react";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface Integration {
  name: string;
  icon: React.ElementType;
  status: "Connected" | "Disconnected" | "Error";
  description: string;
  lastSync?: string;
}

const integrations: Integration[] = [
  { name: "Splunk SIEM", icon: Database, status: "Connected", description: "Log ingestion and correlation engine", lastSync: "2m ago" },
  { name: "CrowdStrike EDR", icon: Shield, status: "Connected", description: "Endpoint detection and response", lastSync: "5m ago" },
  { name: "VirusTotal", icon: Globe, status: "Connected", description: "File and URL threat intelligence", lastSync: "1m ago" },
  { name: "Slack Notifications", icon: Mail, status: "Connected", description: "Alert notifications to SOC channel", lastSync: "Just now" },
  { name: "MISP", icon: Zap, status: "Disconnected", description: "Threat intelligence sharing platform" },
  { name: "TheHive", icon: Monitor, status: "Error", description: "Incident response platform", lastSync: "Failed 1h ago" },
];

const getStatusStyles = (status: string) => {
  switch (status) {
    case "Connected": return { color: "text-secondary", bg: "bg-secondary/10", border: "border-secondary/20", dot: "bg-secondary" };
    case "Disconnected": return { color: "text-muted-foreground", bg: "bg-muted/10", border: "border-white/[0.06]", dot: "bg-muted-foreground" };
    case "Error": return { color: "text-destructive", bg: "bg-destructive/10", border: "border-destructive/20", dot: "bg-destructive" };
    default: return { color: "text-muted-foreground", bg: "bg-muted/10", border: "border-white/[0.06]", dot: "bg-muted-foreground" };
  }
};

const SETTINGS_STORAGE_KEY = "bt_soc_notification_settings_v1";

const DEFAULT_NOTIFICATIONS = {
  criticalAlerts: true,
  highAlerts: true,
  mediumAlerts: false,
  lowAlerts: false,
  incidentUpdates: true,
  systemHealth: true,
  weeklyReport: true,
  emailNotif: true,
  slackNotif: true,
  smsNotif: false,
};

const Settings = () => {
  const [notifications, setNotifications] = useState(() => {
    try {
      const saved = localStorage.getItem(SETTINGS_STORAGE_KEY);
      if (saved) {
        return { ...DEFAULT_NOTIFICATIONS, ...JSON.parse(saved) };
      }
    } catch {
      // Corrupt/unavailable storage -> fall back to defaults.
    }
    return DEFAULT_NOTIFICATIONS;
  });

  const toggleNotif = (key: keyof typeof DEFAULT_NOTIFICATIONS) => {
    setNotifications(prev => {
      const next = { ...prev, [key]: !prev[key] };
      try {
        localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(next));
      } catch {
        // best-effort persistence
      }
      return next;
    });
  };

  const Toggle = ({ checked, onChange }: { checked: boolean; onChange: () => void }) => (
    <button onClick={onChange} className={cn("relative w-10 h-5 rounded-full transition-colors duration-200", checked ? "bg-primary" : "bg-muted/50")}>
      <div className={cn("absolute top-0.5 w-4 h-4 rounded-full bg-foreground transition-transform duration-200", checked ? "left-5" : "left-0.5")} />
    </button>
  );

  return (
    <main className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <div className="flex flex-1 overflow-hidden">
        <SOCSidebar activeItem="Settings" />
        <div className="flex-1 flex flex-col min-w-0">
          <header className="bg-card/25 backdrop-blur-lg border-b border-white/[0.08] px-6 py-4 flex items-center justify-between">
            <div>
              <h1 className="text-xl font-semibold text-foreground">SOC Settings</h1>
              <p className="text-sm text-muted-foreground">Configure integrations, notifications, and preferences</p>
            </div>
            <div className="flex items-center gap-3">
              <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors rounded-lg hover:bg-white/[0.04]"><Bell className="w-5 h-5" /><span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full" /></button>
              <button className="w-8 h-8 bg-primary/10 border border-primary/25 rounded-full flex items-center justify-center text-primary hover:bg-primary/20 transition-colors"><User className="w-4 h-4" /></button>
            </div>
          </header>

          <div className="flex-1 p-6 overflow-auto">
            <div className="max-w-4xl space-y-6">

              {/* Integrations */}
              <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-6 shadow-lg shadow-black/20">
                <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

                <div className="relative pl-3">
                  <div className="flex items-center gap-2 mb-1">
                    <Zap className="w-5 h-5 text-primary" />
                    <h2 className="text-base font-semibold text-foreground">Integrations</h2>
                  </div>
                  <p className="text-xs text-muted-foreground mb-5">Connected tools and data sources</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {integrations.map((integ) => {
                      const styles = getStatusStyles(integ.status);
                      return (
                        <div key={integ.name} className={cn("group p-4 rounded-lg border transition-all duration-200 hover:bg-white/[0.02] cursor-pointer", styles.border)}>
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex items-center gap-2.5">
                              <div className={cn("p-2 rounded-lg", styles.bg)}>
                                <integ.icon className={cn("w-4 h-4", styles.color)} />
                              </div>
                              <div>
                                <h3 className="text-sm font-medium text-foreground">{integ.name}</h3>
                                <p className="text-[10px] text-muted-foreground">{integ.description}</p>
                              </div>
                            </div>
                            <div className="flex items-center gap-1.5">
                              <div className={cn("w-2 h-2 rounded-full", styles.dot, integ.status === "Connected" && "animate-pulse")} />
                              <span className={cn("text-[10px] font-medium", styles.color)}>{integ.status}</span>
                            </div>
                          </div>
                          {integ.lastSync && (
                            <div className="flex items-center gap-1 text-[10px] text-muted-foreground pl-11">
                              <Clock className="w-3 h-3" />
                              <span>Last sync: {integ.lastSync}</span>
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              {/* Notification Preferences */}
              <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-6 shadow-lg shadow-black/20">
                <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

                <div className="relative pl-3">
                  <div className="flex items-center gap-2 mb-1">
                    <Bell className="w-5 h-5 text-primary" />
                    <h2 className="text-base font-semibold text-foreground">Notification Preferences</h2>
                  </div>
                  <p className="text-xs text-muted-foreground mb-5">Configure which alerts trigger notifications</p>

                  <div className="space-y-6">
                    <div>
                      <h3 className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">Alert Severity</h3>
                      <div className="space-y-3">
                        {[
                          { key: "criticalAlerts" as const, label: "Critical Alerts", desc: "Immediate notification for critical severity events", color: "text-destructive" },
                          { key: "highAlerts" as const, label: "High Alerts", desc: "Notification for high severity events", color: "text-orange-400" },
                          { key: "mediumAlerts" as const, label: "Medium Alerts", desc: "Notification for medium severity events", color: "text-yellow-400" },
                          { key: "lowAlerts" as const, label: "Low Alerts", desc: "Notification for low/informational events", color: "text-primary" },
                        ].map((item) => (
                          <div key={item.key} className="flex items-center justify-between p-3 rounded-lg hover:bg-white/[0.02] transition-colors">
                            <div className="flex items-center gap-3">
                              <AlertTriangle className={cn("w-4 h-4", item.color)} />
                              <div>
                                <p className="text-sm text-foreground">{item.label}</p>
                                <p className="text-[10px] text-muted-foreground">{item.desc}</p>
                              </div>
                            </div>
                            <Toggle checked={notifications[item.key]} onChange={() => toggleNotif(item.key)} />
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="border-t border-white/[0.06] pt-5">
                      <h3 className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">Channels</h3>
                      <div className="space-y-3">
                        {[
                          { key: "emailNotif" as const, label: "Email", desc: "Receive notifications via email", icon: Mail },
                          { key: "slackNotif" as const, label: "Slack", desc: "Post to SOC Slack channel", icon: Globe },
                          { key: "smsNotif" as const, label: "SMS", desc: "Text message for critical events", icon: Smartphone },
                        ].map((item) => (
                          <div key={item.key} className="flex items-center justify-between p-3 rounded-lg hover:bg-white/[0.02] transition-colors">
                            <div className="flex items-center gap-3">
                              <item.icon className="w-4 h-4 text-primary" />
                              <div>
                                <p className="text-sm text-foreground">{item.label}</p>
                                <p className="text-[10px] text-muted-foreground">{item.desc}</p>
                              </div>
                            </div>
                            <Toggle checked={notifications[item.key]} onChange={() => toggleNotif(item.key)} />
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="border-t border-white/[0.06] pt-5">
                      <h3 className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">Reports</h3>
                      <div className="space-y-3">
                        {[
                          { key: "incidentUpdates" as const, label: "Incident Updates", desc: "Notify on incident status changes", icon: Shield },
                          { key: "systemHealth" as const, label: "System Health", desc: "Infrastructure health degradation alerts", icon: Monitor },
                          { key: "weeklyReport" as const, label: "Weekly Summary", desc: "Automated weekly threat summary report", icon: SettingsIcon },
                        ].map((item) => (
                          <div key={item.key} className="flex items-center justify-between p-3 rounded-lg hover:bg-white/[0.02] transition-colors">
                            <div className="flex items-center gap-3">
                              <item.icon className="w-4 h-4 text-primary" />
                              <div>
                                <p className="text-sm text-foreground">{item.label}</p>
                                <p className="text-[10px] text-muted-foreground">{item.desc}</p>
                              </div>
                            </div>
                            <Toggle checked={notifications[item.key]} onChange={() => toggleNotif(item.key)} />
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* SOC Team */}
              <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-6 shadow-lg shadow-black/20">
                <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
                <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

                <div className="relative pl-3">
                  <div className="flex items-center gap-2 mb-1">
                    <Users className="w-5 h-5 text-primary" />
                    <h2 className="text-base font-semibold text-foreground">SOC Team</h2>
                  </div>
                  <p className="text-xs text-muted-foreground mb-5">Team members and roles</p>

                  <div className="space-y-3">
                    {[
                      { name: "Sarah Martinez", role: "SOC Lead", status: "Online", incidents: 3, shift: "Day" },
                      { name: "John Davis", role: "Tier 2 Analyst", status: "Online", incidents: 2, shift: "Day" },
                      { name: "Mike Robinson", role: "Tier 2 Analyst", status: "Online", incidents: 1, shift: "Day" },
                      { name: "Emily Chen", role: "Tier 1 Analyst", status: "Offline", incidents: 0, shift: "Night" },
                      { name: "Alex Kumar", role: "Threat Hunter", status: "Offline", incidents: 0, shift: "Night" },
                    ].map((member) => (
                      <div key={member.name} className="flex items-center justify-between p-3 rounded-lg hover:bg-white/[0.02] transition-colors">
                        <div className="flex items-center gap-3">
                          <div className="relative">
                            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-primary/30 to-secondary/20 border border-white/[0.08] flex items-center justify-center text-xs font-bold text-foreground">
                              {member.name.split(" ").map(n => n[0]).join("")}
                            </div>
                            <div className={cn("absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-background", member.status === "Online" ? "bg-secondary" : "bg-muted-foreground")} />
                          </div>
                          <div>
                            <p className="text-sm font-medium text-foreground">{member.name}</p>
                            <p className="text-[10px] text-muted-foreground">{member.role} · {member.shift} shift</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-3">
                          {member.incidents > 0 && (
                            <span className="text-[10px] text-muted-foreground flex items-center gap-1">
                              <Shield className="w-3 h-3" />{member.incidents} active
                            </span>
                          )}
                          <span className={cn("text-[10px]", member.status === "Online" ? "text-secondary" : "text-muted-foreground")}>{member.status}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Settings;
