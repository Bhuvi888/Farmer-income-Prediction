import { useState, useRef } from "react";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import StatsTicker from "./components/StatsTicker";
import PredictionForm from "./components/PredictionForm";
import ResultCard, { ResultSkeleton } from "./components/ResultCard";
import ChartsSection from "./components/ChartsSection";
import InsightPanel from "./components/InsightPanel";
import Footer from "./components/Footer";

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState(null);
  const resultRef = useRef(null);

  const handlePredict = async (data) => {
    setIsLoading(true);
    setResult(null);
    setFormData(data);

    // Smooth scroll to results area
    setTimeout(() => {
      resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);

    try {
      // Try real API first, fallback to mock
      // const res = await axios.post("/api/predict", data);
      // setResult(res.data);

      // Mock prediction (simulate API delay)
      await new Promise((r) => setTimeout(r, 1500));

      const landSize = Number(data.land_size);
      const yieldPerAcre = Number(data.yield_per_acre);
      const marketPrice = Number(data.market_price);
      const irrigated = Number(data.irrigated_percentage);
      const distance = Number(data.market_distance);

      // Simple mock formula for demo
      const baseIncome = landSize * yieldPerAcre * marketPrice;
      const irrigationBonus = baseIncome * (irrigated / 100) * 0.15;
      const distancePenalty = distance * 500;
      const predicted = Math.round(
        baseIncome + irrigationBonus - distancePenalty + 50000,
      );

      const eligibility =
        predicted > 800000 ? "High" : predicted > 400000 ? "Medium" : "Low";

      setResult({
        predicted_income: Math.max(predicted, 30000),
        loan_eligibility: eligibility,
      });
    } catch (err) {
      console.error("Prediction failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <StatsTicker />
      <HeroSection />

      <main className="flex-1">
        <PredictionForm onSubmit={handlePredict} isLoading={isLoading} />

        {/* Results area */}
        <div
          ref={resultRef}
          className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-16 space-y-8"
        >
          {isLoading && <ResultSkeleton />}
          {!isLoading && result && (
            <>
              <ResultCard result={result} />
              <ChartsSection show={!!result} />
              <InsightPanel formData={formData} show={!!result} />
            </>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
