import { Lightbulb, TrendingUp, AlertTriangle, Leaf } from "lucide-react";

function generateInsights(formData) {
  const insights = [];

  const irrigated = Number(formData?.irrigated_percentage || 0);
  const distance = Number(formData?.market_distance || 0);
  const yieldPerAcre = Number(formData?.yield_per_acre || 0);
  const rainfall = Number(formData?.rainfall || 0);
  const landSize = Number(formData?.land_size || 0);

  // Irrigation insight
  if (irrigated >= 70) {
    insights.push({
      icon: TrendingUp,
      color: "text-green-600 bg-green-50",
      title: "Strong irrigation coverage",
      desc: `${irrigated}% irrigated land ensures consistent crop growth and higher income potential.`,
    });
  } else if (irrigated < 40) {
    insights.push({
      icon: AlertTriangle,
      color: "text-amber-600 bg-amber-50",
      title: "Low irrigation coverage",
      desc: `Only ${irrigated}% of land is irrigated. Consider investing in drip or sprinkler systems to boost yield.`,
    });
  }

  // Market distance insight
  if (distance > 20) {
    insights.push({
      icon: AlertTriangle,
      color: "text-amber-600 bg-amber-50",
      title: "Market distance reduces profitability",
      desc: `At ${distance}km from the nearest mandi, transportation costs may cut into profits.`,
    });
  } else {
    insights.push({
      icon: TrendingUp,
      color: "text-green-600 bg-green-50",
      title: "Good market accessibility",
      desc: `Only ${distance}km from the nearest mandi — low transport costs support better margins.`,
    });
  }

  // Crop yield insight
  if (yieldPerAcre >= 15) {
    insights.push({
      icon: Leaf,
      color: "text-green-600 bg-green-50",
      title: "High crop yield potential",
      desc: `Yield of ${yieldPerAcre} quintals/acre indicates productive farming with good practices.`,
    });
  } else {
    insights.push({
      icon: Lightbulb,
      color: "text-blue-600 bg-blue-50",
      title: "Yield improvement opportunity",
      desc: `Current yield of ${yieldPerAcre} quintals/acre can be improved with better seed varieties and fertilization.`,
    });
  }

  // Rainfall
  if (rainfall > 1000) {
    insights.push({
      icon: AlertTriangle,
      color: "text-amber-600 bg-amber-50",
      title: "High rainfall risk",
      desc: `Rainfall of ${rainfall}mm may cause waterlogging. Ensure proper drainage systems.`,
    });
  }

  // Land size
  if (landSize > 5) {
    insights.push({
      icon: TrendingUp,
      color: "text-green-600 bg-green-50",
      title: "Large landholding advantage",
      desc: `${landSize} acres provides economies of scale for mechanized farming.`,
    });
  }

  return insights.slice(0, 3);
}

export default function InsightPanel({ formData, show }) {
  if (!show) return null;

  const insights = generateInsights(formData);

  return (
    <div id="insights" className="animate-fade-in-up">
      <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
        <Lightbulb className="w-5 h-5 text-primary-500" />
        Smart Insights
      </h3>
      <div className="grid sm:grid-cols-3 gap-4">
        {insights.map((insight, i) => (
          <div
            key={i}
            className="bg-white rounded-2xl shadow-md shadow-gray-100 border border-gray-100 p-5 hover:shadow-lg transition-shadow"
          >
            <div
              className={`w-9 h-9 rounded-xl ${insight.color} flex items-center justify-center mb-3`}
            >
              <insight.icon className="w-4.5 h-4.5" />
            </div>
            <h4 className="text-sm font-semibold text-gray-800 mb-1">
              {insight.title}
            </h4>
            <p className="text-xs text-gray-500 leading-relaxed">
              {insight.desc}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
