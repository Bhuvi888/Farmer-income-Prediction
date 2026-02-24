import { Sprout } from "lucide-react";

export default function Footer() {
  return (
    <footer id="about" className="bg-gray-900 text-gray-400">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-3 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
                <Sprout className="w-4 h-4 text-white" />
              </div>
              <span className="text-lg font-bold text-white">
                Agri<span className="text-primary-400">Predict</span> AI
              </span>
            </div>
            <p className="text-sm leading-relaxed">
              AI for Financial Inclusion in Agriculture. Empowering lenders and
              farmers with data-driven income predictions.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-sm font-semibold text-white mb-3">
              Quick Links
            </h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a
                  href="#dashboard"
                  className="hover:text-primary-400 transition"
                >
                  Dashboard
                </a>
              </li>
              <li>
                <a
                  href="#prediction"
                  className="hover:text-primary-400 transition"
                >
                  Prediction
                </a>
              </li>
              <li>
                <a
                  href="#insights"
                  className="hover:text-primary-400 transition"
                >
                  Insights
                </a>
              </li>
            </ul>
          </div>

          {/* Tech */}
          <div>
            <h4 className="text-sm font-semibold text-white mb-3">
              Tech Stack
            </h4>
            <div className="flex flex-wrap gap-2">
              {[
                "React",
                "Vite",
                "Tailwind CSS",
                "LightGBM",
                "Python",
                "Recharts",
              ].map((t) => (
                <span
                  key={t}
                  className="px-2.5 py-1 bg-gray-800 rounded-lg text-xs text-gray-300"
                >
                  {t}
                </span>
              ))}
            </div>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-6 text-center text-xs text-gray-500">
          
          {new Date().getFullYear()} AgriPredict AI
        </div>
      </div>
    </footer>
  );
}
