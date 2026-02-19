import { useState, useRef } from "react";
import axios from "axios";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import StatsTicker from "./components/StatsTicker";
import PredictionForm from "./components/PredictionForm";
import ResultCard, { ResultSkeleton } from "./components/ResultCard";
import ChartsSection from "./components/ChartsSection";
import InsightPanel from "./components/InsightPanel";
import Footer from "./components/Footer";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

function App() {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState(null);
  const [error, setError] = useState(null);
  const resultRef = useRef(null);

  const handlePredict = async (data) => {
    setIsLoading(true);
    setResult(null);
    setError(null);
    setFormData(data);

    // Smooth scroll to results area
    setTimeout(() => {
      resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);

    try {
      const res = await axios.post(`${API_URL}/api/predict`, data);
      setResult(res.data);
    } catch (err) {
      console.error("Prediction failed:", err);
      setError("Prediction failed. Make sure the backend server is running.");
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

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-5 py-4 rounded-xl text-sm animate-fade-in-up">
              ⚠️ {error}
            </div>
          )}

          {!isLoading && result && (
            <>
              <ResultCard result={result} />
              <ChartsSection show={!!result} result={result} />
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
