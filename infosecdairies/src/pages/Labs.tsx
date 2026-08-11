import Navbar from "@/components/Navbar";
import SOCSidebar from "@/components/soc/SOCSidebar";
import AlertSummaryCards from "@/components/soc/AlertSummaryCards";
import AlertsChart from "@/components/soc/AlertsChart";
import TopSourcesChart from "@/components/soc/TopSourcesChart";
import RecentAlertsTable from "@/components/soc/RecentAlertsTable";
import SeverityDonutChart from "@/components/soc/SeverityDonutChart";
import ActiveInvestigations from "@/components/soc/ActiveInvestigations";
import MitreHeatmapInteractive from "@/components/soc/MitreHeatmapInteractive";
import ThreatGeoMap from "@/components/soc/ThreatGeoMap";
import LiveActivityFeed from "@/components/soc/LiveActivityFeed";

import { Bell, Search, User, RefreshCw, Clock } from "lucide-react";

const Labs = () => {
  return (
    <main className="min-h-screen bg-background flex flex-col">
      <Navbar />

      <div className="flex flex-1 overflow-hidden relative">
        <SOCSidebar activeItem="Dashboard" />
        <div className="flex-1 flex flex-col min-w-0">
            <header className="bg-card/25 backdrop-blur-lg border-b border-white/[0.08] px-6 py-4 flex items-center justify-between">
              <div>
                <h1 className="text-xl font-semibold text-foreground">Security Dashboard</h1>
                <p className="text-sm text-muted-foreground flex items-center gap-2">
                  Real-time threat monitoring and analysis
                  <span className="flex items-center gap-1 text-[10px] text-primary/60">
                    <Clock className="w-3 h-3" />
                    Last updated: just now
                  </span>
                </p>
              </div>
              <div className="flex items-center gap-3">
                <div className="relative hidden md:block">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <input
                    type="text"
                    placeholder="Search alerts, IPs, IOCs..."
                    className="bg-background/50 border border-white/[0.08] rounded-lg pl-10 pr-4 py-2 text-sm text-foreground placeholder:text-muted-foreground w-72"
                    readOnly
                  />
                </div>
                <button className="p-2 text-muted-foreground rounded-lg"><RefreshCw className="w-4 h-4" /></button>
                <button className="relative p-2 text-muted-foreground rounded-lg"><Bell className="w-5 h-5" /><span className="absolute top-1 right-1 w-2 h-2 bg-destructive rounded-full" /></button>
                <button className="w-8 h-8 bg-primary/10 border border-primary/25 rounded-full flex items-center justify-center text-primary"><User className="w-4 h-4" /></button>
              </div>
            </header>
            <div className="flex-1 p-6 overflow-hidden">
              <div className="space-y-6">
                <AlertSummaryCards />
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-2"><AlertsChart /></div>
                  <div className="lg:col-span-1"><LiveActivityFeed /></div>
                </div>
                <MitreHeatmapInteractive />
                <ThreatGeoMap />
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="lg:col-span-1"><TopSourcesChart /></div>
                  <div className="lg:col-span-1"><ActiveInvestigations /></div>
                  <div className="lg:col-span-1"><SeverityDonutChart /></div>
                </div>
                <RecentAlertsTable />
              </div>
            </div>
          </div>
      </div>
    </main>
  );
};

export default Labs;
