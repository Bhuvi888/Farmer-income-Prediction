import { IndianRupee, ShieldCheck, ShieldAlert, ShieldX } from "lucide-react";
import { cn } from "../lib/utils";

const eligibilityConfig = {
  High: {
    color: "bg-green-50 text-green-700 border-green-200",
    icon: ShieldCheck,
    label: "High Eligibility",
  },
  Medium: {
    color: "bg-amber-50 text-amber-700 border-amber-200",
    icon: ShieldAlert,
    label: "Medium Eligibility",
  },
  Low: {
    color: "bg-red-50 text-red-700 border-red-200",
    icon: ShieldX,
    label: "Low Eligibility",
  },
};

export default function ResultCard({ result }) {
  if (!result) return null;

  const income = result.predicted_income;
  const eligibility = result.loan_eligibility || "Medium";
  const config = eligibilityConfig[eligibility];
  const Icon = config.icon;

  const formatted = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(income);

  return (
    <div className="animate-fade-in-up bg-white rounded-2xl shadow-lg shadow-gray-200/50 border border-gray-100 p-6 sm:p-8">
      <div className="text-center">
        <p className="text-sm text-gray-400 font-medium mb-1">
          Predicted Annual Income
        </p>
        <div className="flex items-center justify-center gap-2">
          <IndianRupee className="w-8 h-8 text-primary-500" />
          <span className="text-4xl sm:text-5xl font-extrabold text-gray-900">
            {formatted.replace("₹", "")}
          </span>
        </div>

        <div className="mt-5 flex flex-wrap items-center justify-center gap-3">
          <div
            className={cn(
              "flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-semibold",
              config.color,
            )}
          >
            <Icon className="w-4 h-4" />
            {config.label}
          </div>

          <div className="flex items-center gap-2 px-3 py-2 rounded-xl border border-gray-100 bg-gray-50/50 text-[10px] font-medium text-gray-500">
            <span className="opacity-60">Engine:</span> {result.model_version}
          </div>
          <div className="flex items-center gap-2 px-3 py-2 rounded-xl border border-gray-100 bg-gray-50/50 text-[10px] font-medium text-gray-500">
            <span className="opacity-60">Features:</span> {result.features_used}
          </div>
        </div>
      </div>
    </div>
  );
}

export function ResultSkeleton() {
  return (
    <div className="bg-white rounded-2xl shadow-lg shadow-gray-200/50 border border-gray-100 p-8">
      <div className="flex flex-col items-center gap-4">
        <div className="skeleton w-48 h-4" />
        <div className="skeleton w-64 h-12" />
        <div className="skeleton w-36 h-8 mt-2" />
      </div>
    </div>
  );
}
