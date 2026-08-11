import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

const data = [
  { name: "Critical", value: 12, color: "hsl(0, 84%, 60%)" },
  { name: "High", value: 47, color: "hsl(25, 95%, 53%)" },
  { name: "Medium", value: 156, color: "hsl(48, 96%, 53%)" },
  { name: "Low", value: 1032, color: "hsl(186, 100%, 42%)" },
];

const SeverityDonutChart = () => {
  const total = data.reduce((sum, d) => sum + d.value, 0);

  return (
    <div className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-5 shadow-lg shadow-black/20 hover:bg-card/35 hover:border-white/[0.12] transition-all duration-300">
      <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/15 to-transparent" />
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

      <div className="relative pl-2">
        <div className="mb-4">
          <h3 className="text-sm font-semibold text-foreground">Severity Distribution</h3>
          <p className="text-xs text-muted-foreground mt-0.5">Alert breakdown by severity</p>
        </div>

        <div className="flex items-center gap-6">
          <div className="relative w-36 h-36 flex-shrink-0">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={60}
                  paddingAngle={3}
                  dataKey="value"
                  strokeWidth={0}
                >
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
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
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-lg font-bold text-foreground">{total.toLocaleString()}</span>
              <span className="text-[10px] text-muted-foreground">Total</span>
            </div>
          </div>

          <div className="flex-1 space-y-3">
            {data.map((item) => (
              <div key={item.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-xs text-muted-foreground">{item.name}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-medium text-foreground">{item.value}</span>
                  <span className="text-[10px] text-muted-foreground/60">
                    ({((item.value / total) * 100).toFixed(1)}%)
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SeverityDonutChart;
