import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const data = [
  { time: "00:00", critical: 2, high: 5, medium: 12, low: 24 },
  { time: "04:00", critical: 1, high: 3, medium: 8, low: 18 },
  { time: "08:00", critical: 4, high: 8, medium: 18, low: 45 },
  { time: "12:00", critical: 6, high: 12, medium: 28, low: 78 },
  { time: "16:00", critical: 3, high: 15, medium: 32, low: 92 },
  { time: "20:00", critical: 5, high: 9, medium: 22, low: 56 },
  { time: "Now", critical: 4, high: 11, medium: 25, low: 67 },
];

const AlertsChart = () => {
  return (
    <div className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 hover:bg-card/35 hover:border-white/[0.12] transition-all duration-300">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

      <div className="relative pl-2">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h3 className="text-sm font-semibold text-foreground">Alert Trends (24h)</h3>
            <p className="text-xs text-muted-foreground mt-0.5">Breakdown by severity level</p>
          </div>
          <div className="flex items-center gap-3">
            {[
              { label: "Critical", color: "bg-destructive" },
              { label: "High", color: "bg-orange-500" },
              { label: "Medium", color: "bg-yellow-500" },
              { label: "Low", color: "bg-primary" },
            ].map((item) => (
              <div key={item.label} className="flex items-center gap-1.5">
                <div className={`w-2 h-2 rounded-full ${item.color}`} />
                <span className="text-[10px] text-muted-foreground">{item.label}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <defs>
                <linearGradient id="critGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="hsl(0, 84%, 60%)" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="hsl(0, 84%, 60%)" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="highGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="hsl(25, 95%, 53%)" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="hsl(25, 95%, 53%)" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="medGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="hsl(48, 96%, 53%)" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="hsl(48, 96%, 53%)" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="lowGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="hsl(186, 100%, 42%)" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="hsl(186, 100%, 42%)" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(220, 30%, 15%)" />
              <XAxis
                dataKey="time"
                stroke="hsl(180, 20%, 45%)"
                fontSize={10}
                tickLine={false}
              />
              <YAxis
                stroke="hsl(180, 20%, 45%)"
                fontSize={10}
                tickLine={false}
                axisLine={false}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(220, 35%, 10%)",
                  border: "1px solid hsl(220, 30%, 20%)",
                  borderRadius: "10px",
                  color: "hsl(180, 100%, 95%)",
                  fontSize: "12px",
                  boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
                }}
              />
              <Area type="monotone" dataKey="low" stroke="hsl(186, 100%, 42%)" strokeWidth={1.5} fill="url(#lowGrad)" />
              <Area type="monotone" dataKey="medium" stroke="hsl(48, 96%, 53%)" strokeWidth={1.5} fill="url(#medGrad)" />
              <Area type="monotone" dataKey="high" stroke="hsl(25, 95%, 53%)" strokeWidth={1.5} fill="url(#highGrad)" />
              <Area type="monotone" dataKey="critical" stroke="hsl(0, 84%, 60%)" strokeWidth={2} fill="url(#critGrad)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AlertsChart;
