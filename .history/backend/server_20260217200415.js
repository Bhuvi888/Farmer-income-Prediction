const express = require("express");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 5000;

// ── Middleware ──────────────────────────────────────────────
app.use(cors());
app.use(express.json());

// ── Health check ───────────────────────────────────────────
app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

// ── Predict endpoint ───────────────────────────────────────
app.post("/api/predict", (req, res) => {
  const {
    land_size,
    irrigated_percentage,
    soil_type,
    crop_type,
    season,
    yield_per_acre,
    rainfall,
    temperature,
    market_price,
    market_distance,
  } = req.body;

  // --- Validate required fields ---
  const missing = [];
  if (!land_size) missing.push("land_size");
  if (!crop_type) missing.push("crop_type");
  if (!yield_per_acre) missing.push("yield_per_acre");
  if (!market_price) missing.push("market_price");

  if (missing.length > 0) {
    return res
      .status(400)
      .json({ error: `Missing fields: ${missing.join(", ")}` });
  }

  // --- Mock prediction logic ---
  // (replace this with actual Python model call later)
  const ls = Number(land_size);
  const ypa = Number(yield_per_acre);
  const mp = Number(market_price);
  const irr = Number(irrigated_percentage) || 50;
  const dist = Number(market_distance) || 10;
  const rain = Number(rainfall) || 800;
  const temp = Number(temperature) || 28;

  // Crop multiplier
  const cropMultipliers = {
    Rice: 1.0,
    Wheat: 0.95,
    Sugarcane: 1.3,
    Cotton: 1.1,
    Maize: 0.85,
    Soybean: 0.9,
    Pulses: 0.8,
    Groundnut: 1.05,
    Vegetables: 1.25,
  };
  const cropMul = cropMultipliers[crop_type] || 1.0;

  // Season multiplier
  const seasonMultipliers = { Kharif: 1.05, Rabi: 1.0, Zaid: 0.9 };
  const seasonMul = seasonMultipliers[season] || 1.0;

  // Soil quality factor
  const soilFactors = {
    Alluvial: 1.1,
    "Black Cotton": 1.15,
    Loamy: 1.05,
    Clay: 0.95,
    Red: 0.9,
    Sandy: 0.8,
    Laterite: 0.85,
  };
  const soilFactor = soilFactors[soil_type] || 1.0;

  // Base income calculation
  let income = ls * ypa * mp * cropMul * seasonMul * soilFactor;

  // Irrigation bonus (up to +20%)
  income *= 1 + (irr / 100) * 0.2;

  // Distance penalty (₹800 per km)
  income -= dist * 800;

  // Rainfall effect (optimal: 600-1000mm)
  if (rain < 400) income *= 0.8;
  else if (rain > 1200) income *= 0.85;

  // Temperature effect (optimal: 22-32°C)
  if (temp < 15 || temp > 40) income *= 0.85;

  // Floor
  income = Math.max(Math.round(income), 25000);

  // Loan eligibility
  let loan_eligibility;
  if (income >= 800000) loan_eligibility = "High";
  else if (income >= 350000) loan_eligibility = "Medium";
  else loan_eligibility = "Low";

  // Simulate slight delay (like real model inference)
  setTimeout(() => {
    res.json({
      predicted_income: income,
      loan_eligibility,
      model_version: "v2.0",
      features_used: 286,
    });
  }, 500);
});

// ── Start server ───────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`\n  🚀 AgriPredict API running on http://localhost:${PORT}`);
  console.log(`  📡 POST /api/predict`);
  console.log(`  ❤️  GET  /api/health\n`);
});
