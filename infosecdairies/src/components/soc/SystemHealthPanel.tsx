import { Activity, Server, Wifi, Database, Cpu, HardDrive, CheckCircle, AlertTriangle } from "lucide-react";

const systems = [
  { name: "SIEM Cluster", icon: Server, status: "operational", uptime: "99.97%", cpu: 42, memory: 68 },
  { name: "Network Sensors", icon: Wifi, status: "operational", uptime: "99.99%", cpu: 28, memory: 45 },
  { name: "Log Collector", icon: Database, status: "degraded", uptime: "98.50%", cpu: 89, memory: 92 },
  { name: "Threat Intel Feed", icon: Activity, status: "operational", uptime: "99.95%", cpu: 15, memory: 32 },
  { name: "EDR Agents", icon: Cpu, status: "operational", uptime: "99.98%", cpu: 35, memory: 55 },
  { name: "Backup Storage", icon: HardDrive, status: "operational", uptime: "100%", cpu: 12, memory: 78 },
];

const SystemHealthPanel = () => {
  const operationalCount = systems.filter(s => s.status === "operational").length;

  return (
    <div className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 hover:bg-card/35 hover:border-white/[0.12] transition-all duration-300">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

      <div className="relative pl-2">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h3 className="text-sm font-semibold text-foreground">System Health</h3>
            <p className="text-xs text-muted-foreground mt-0.5">Infrastructure monitoring status</p>
          </div>
          <span className="flex items-center gap-1.5 text-xs text-secondary px-2.5 py-1 rounded-full bg-secondary/10 border border-secondary/20">
            <CheckCircle className="w-3 h-3" />
            {operationalCount}/{systems.length} Online
          </span>
        </div>

        <div className="space-y-3">
          {systems.map((system) => (
            <div key={system.name} className="flex items-center gap-3 p-2.5 rounded-lg hover:bg-white/[0.02] transition-colors">
              <div className={`p-1.5 rounded-md ${system.status === "operational" ? "bg-primary/10" : "bg-yellow-500/10"}`}>
                <system.icon className={`w-3.5 h-3.5 ${system.status === "operational" ? "text-primary" : "text-yellow-400"}`} />
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-medium text-foreground">{system.name}</span>
                  <div className="flex items-center gap-1">
                    {system.status === "operational"
                      ? <CheckCircle className="w-3 h-3 text-secondary" />
                      : <AlertTriangle className="w-3 h-3 text-yellow-400" />
                    }
                    <span className={`text-[10px] ${system.status === "operational" ? "text-secondary" : "text-yellow-400"}`}>
                      {system.uptime}
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <div className="flex items-center gap-1.5 flex-1">
                    <span className="text-[9px] text-muted-foreground/60 w-7">CPU</span>
                    <div className="flex-1 h-1 bg-muted/30 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${system.cpu > 80 ? "bg-destructive" : system.cpu > 60 ? "bg-yellow-500" : "bg-primary"}`}
                        style={{ width: `${system.cpu}%` }}
                      />
                    </div>
                    <span className="text-[9px] text-muted-foreground/60 w-7 text-right">{system.cpu}%</span>
                  </div>
                  <div className="flex items-center gap-1.5 flex-1">
                    <span className="text-[9px] text-muted-foreground/60 w-7">MEM</span>
                    <div className="flex-1 h-1 bg-muted/30 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${system.memory > 80 ? "bg-destructive" : system.memory > 60 ? "bg-yellow-500" : "bg-secondary"}`}
                        style={{ width: `${system.memory}%` }}
                      />
                    </div>
                    <span className="text-[9px] text-muted-foreground/60 w-7 text-right">{system.memory}%</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SystemHealthPanel;
