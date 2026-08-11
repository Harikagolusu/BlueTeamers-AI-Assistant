import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

const data = [
  { source: "192.168.1.105", count: 156, label: "Brute Force" },
  { source: "10.0.0.42", count: 124, label: "Data Exfil" },
  { source: "admin_user", count: 98, label: "Susp. DNS" },
  { source: "WKS-PC-0127", count: 87, label: "PowerShell" },
  { source: "172.16.0.88", count: 65, label: "Port Scan" },
];

const colors = [
  "hsl(0, 84%, 60%)",
  "hsl(25, 95%, 53%)",
  "hsl(48, 96%, 53%)",
  "hsl(84, 81%, 44%)",
  "hsl(186, 100%, 42%)",
];

const TopSourcesChart = () => {
  return (
    <div className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 hover:bg-card/35 hover:border-white/[0.12] transition-all duration-300">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

      <div className="relative pl-2">
        <div className="flex items-center justify-between mb-5">
          <div>
            <h3 className="text-sm font-semibold text-foreground">Top Alert Sources</h3>
            <p className="text-xs text-muted-foreground mt-0.5">Most active threat origins</p>
          </div>
        </div>
        <div className="h-56">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="vertical" barCategoryGap="20%">
              <XAxis
                type="number"
                stroke="hsl(180, 20%, 45%)"
                fontSize={10}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                type="category"
                dataKey="source"
                stroke="hsl(180, 20%, 45%)"
                fontSize={10}
                tickLine={false}
                axisLine={false}
                width={100}
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
              <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default TopSourcesChart;
