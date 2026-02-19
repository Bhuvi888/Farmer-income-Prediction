import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

const COLORS = ["#10b981", "#f59e0b", "#ef4444", "#6366f1", "#8b5cf6"];

const costProfitData = [
  { name: "Net Profit", value: 58 },
  { name: "Seed & Fertilizer", value: 15 },
  { name: "Labour", value: 12 },
  { name: "Machinery", value: 8 },
  { name: "Other Costs", value: 7 },
];

const featureData = [
  { name: "Land Size", contribution: 85 },
  { name: "Crop Yield", contribution: 72 },
  { name: "Market Price", contribution: 60 },
  { name: "Rainfall", contribution: 45 },
  { name: "Irrigation", contribution: 40 },
  { name: "Temperature", contribution: 28 },
  { name: "Soil Type", contribution: 20 },
];

export default function ChartsSection({ show }) {
  if (!show) return null;

  return (
    <div className="animate-fade-in-up grid md:grid-cols-2 gap-6">
      {/* Pie: Cost vs Profit */}
      <div className="bg-white rounded-2xl shadow-lg shadow-gray-200/50 border border-gray-100 p-6">
        <h3 className="text-sm font-semibold text-gray-800 mb-4">
          Cost vs Profit Breakdown
        </h3>
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie
              data={costProfitData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              paddingAngle={3}
              dataKey="value"
            >
              {costProfitData.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                borderRadius: 12,
                border: "1px solid #e5e7eb",
                fontSize: 13,
              }}
              formatter={(val) => `${val}%`}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="flex flex-wrap gap-3 mt-2 justify-center">
          {costProfitData.map((d, i) => (
            <div
              key={d.name}
              className="flex items-center gap-1.5 text-xs text-gray-500"
            >
              <span
                className="w-2.5 h-2.5 rounded-full"
                style={{ background: COLORS[i] }}
              />
              {d.name}
            </div>
          ))}
        </div>
      </div>

      {/* Bar: Feature Contribution */}
      <div className="bg-white rounded-2xl shadow-lg shadow-gray-200/50 border border-gray-100 p-6">
        <h3 className="text-sm font-semibold text-gray-800 mb-4">
          Feature Contribution
        </h3>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={featureData} layout="vertical" margin={{ left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 12 }} />
            <YAxis
              type="category"
              dataKey="name"
              tick={{ fontSize: 12 }}
              width={80}
            />
            <Tooltip
              contentStyle={{
                borderRadius: 12,
                border: "1px solid #e5e7eb",
                fontSize: 13,
              }}
              formatter={(val) => `${val}%`}
            />
            <Bar
              dataKey="contribution"
              fill="#10b981"
              radius={[0, 6, 6, 0]}
              barSize={18}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
