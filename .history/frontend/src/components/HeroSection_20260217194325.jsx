import { ArrowRight, BarChart3, Brain, Shield } from "lucide-react";

export default function HeroSection() {
  return (
    <section
      id="dashboard"
      className="relative overflow-hidden bg-linear-to-br from-primary-50 via-white to-primary-50/30"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left — Text */}
          <div className="animate-fade-in-up">
            <div className="inline-flex items-center gap-2 bg-primary-100 text-primary-700 px-3 py-1.5 rounded-full text-xs font-semibold mb-6">
              <span className="w-2 h-2 rounded-full bg-primary-500 animate-pulse-dot" />
              Powered by Machine Learning
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-gray-900 leading-tight">
              AI-Based
              <span className="text-primary-600 block">Farmer Income</span>
              Prediction
            </h1>

            <p className="mt-6 text-lg text-gray-500 max-w-lg leading-relaxed">
              Empowering financial institutions to assess farmer
              creditworthiness with machine learning — driving{" "}
              <strong className="text-gray-700">financial inclusion</strong> in
              agriculture.
            </p>

            <div className="mt-8 flex flex-wrap gap-4">
              <a
                href="#prediction"
                className="inline-flex items-center gap-2 bg-primary-600 text-white px-6 py-3.5 rounded-xl font-semibold text-sm hover:bg-primary-700 shadow-lg shadow-primary-600/25 hover:shadow-primary-700/30 transition-all hover:-translate-y-0.5"
              >
                Start Prediction
                <ArrowRight className="w-4 h-4" />
              </a>
              <a
                href="#about"
                className="inline-flex items-center gap-2 bg-white text-gray-700 px-6 py-3.5 rounded-xl font-semibold text-sm border border-gray-200 hover:border-primary-300 hover:text-primary-700 transition-all"
              >
                Learn More
              </a>
            </div>
          </div>

          {/* Right — Visual card */}
          <div
            className="hidden lg:flex justify-center animate-fade-in-up"
            style={{ animationDelay: "0.2s" }}
          >
            <div className="relative w-full max-w-md">
              {/* Main card */}
              <div className="bg-white rounded-2xl shadow-xl shadow-gray-200/50 border border-gray-100 p-8">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-10 h-10 rounded-xl bg-primary-100 flex items-center justify-center">
                    <Brain className="w-5 h-5 text-primary-600" />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-800">
                      Income Analysis
                    </p>
                    <p className="text-xs text-gray-400">
                      Real-time prediction
                    </p>
                  </div>
                </div>

                {/* Mock bars */}
                <div className="space-y-4">
                  {[
                    { label: "Land Size", w: "85%", color: "bg-primary-500" },
                    { label: "Crop Yield", w: "72%", color: "bg-primary-400" },
                    {
                      label: "Market Price",
                      w: "60%",
                      color: "bg-primary-300",
                    },
                    { label: "Rainfall", w: "45%", color: "bg-primary-200" },
                  ].map((bar) => (
                    <div key={bar.label}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-gray-500">{bar.label}</span>
                        <span className="text-gray-400">{bar.w}</span>
                      </div>
                      <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full ${bar.color} rounded-full`}
                          style={{ width: bar.w }}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                {/* Mock result */}
                <div className="mt-6 pt-6 border-t border-gray-100 flex items-center justify-between">
                  <div>
                    <p className="text-xs text-gray-400">Predicted Income</p>
                    <p className="text-2xl font-bold text-primary-600">
                      ₹12,54,000
                    </p>
                  </div>
                  <div className="flex items-center gap-1.5 bg-green-50 text-green-700 px-3 py-1.5 rounded-lg text-xs font-semibold">
                    <Shield className="w-3.5 h-3.5" />
                    Eligible
                  </div>
                </div>
              </div>

              {/* Floating badge */}
              <div className="absolute -top-4 -right-4 bg-white rounded-xl shadow-lg shadow-gray-200/50 border border-gray-100 px-4 py-3 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-primary-500" />
                <div>
                  <p className="text-xs text-gray-400">Accuracy</p>
                  <p className="text-sm font-bold text-gray-800">98.4%</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
