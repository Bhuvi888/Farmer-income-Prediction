import { TrendingUp, Users, Clock, Cpu, Leaf, ShieldCheck } from "lucide-react";

const items = [
  { icon: TrendingUp, label: "Model Accuracy", value: "98.4%" },
  { icon: Users, label: "Farmers Supported", value: "12,540+" },
  { icon: Clock, label: "Avg Prediction Time", value: "0.8s" },
  { icon: Cpu, label: "Features Analyzed", value: "286" },
  { icon: Leaf, label: "Crops Covered", value: "50+" },
  { icon: ShieldCheck, label: "Loan Predictions", value: "8,920+" },
];

export default function StatsTicker() {
  return (
    <div className="bg-primary-900 text-white overflow-hidden">
      <div className="flex animate-ticker whitespace-nowrap py-3">
        {/* Duplicate items for seamless loop */}
        {[...items, ...items].map((item, i) => (
          <div key={i} className="inline-flex items-center gap-2 mx-8">
            <item.icon className="w-4 h-4 text-primary-300" />
            <span className="text-xs text-primary-200 font-medium">
              {item.label}:
            </span>
            <span className="text-sm font-bold">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
