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

export default function ChartsSection({ show, result }) {
  if (!show || !result) return null;

  const income = result.predicted_income || 0;

  // Calculate dynamic cost vs profit based on income
  // Assuming ~60% margin for farmers as per our backend heuristics
  const profit = Math.round(income * 0.62);
  const costs = income - profit;

  const costProfitData = [
    { name: "Net Profit", value: profit },
    { name: "Seed & Fertilizer", value: Math.round(costs * 0.4) },
    { name: "Labour", value: Math.round(costs * 0.3) },
    { name: "Machinery", value: Math.round(costs * 0.2) },
    { name: "Other Costs", value: Math.round(costs * 0.1) },
  ];

  // Map 5-fold predictions to chart data
  const featureData = (result.fold_predictions || []).map((val, i) => ({
    name: `Fold ${i + 1}`,
    value: val,
  }));

  return (
    <div className="animate-fade-in-up grid md:grid-cols-2 gap-6">
      {/* Pie: Cost vs Profit */}
      <div className="bg-white rounded-2xl shadow-lg shadow-gray-200/50 border border-gray-100 p-6">
        <h3 className="text-sm font-semibold text-gray-800 mb-4">
          Estimated Cost vs Profit (₹)
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
              formatter={(val) => `₹${val.toLocaleString()}`}
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

      {/* Bar: Model Stability (Fold Predictions) */}
      <div className="bg-white rounded-2xl shadow-lg shadow-gray-200/50 border border-gray-100 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-semibold text-gray-800">
            Model Stability (5-Fold Predictions)
          </h3>
          <span className="text-[10px] bg-gray-100 px-2 py-0.5 rounded-full text-gray-500">
            Ensemble Consistency
          </span>
        </div>
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={featureData} layout="vertical" margin={{ left: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis type="number" tick={{ fontSize: 10 }} hide />
            <YAxis
              type="category"
              dataKey="name"
              tick={{ fontSize: 11 }}
              width={50}
            />
            <Tooltip
              contentStyle={{
                borderRadius: 12,
                border: "1px solid #e5e7eb",
                fontSize: 13,
              }}
              formatter={(val) => `₹${val.toLocaleString()}`}
              cursor={{ fill: "#f9fafb" }}
            />
            <Bar
              dataKey="value"
              fill="#10b981"
              radius={[0, 6, 6, 0]}
              barSize={24}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
