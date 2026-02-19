import { useState } from "react";
import { useForm } from "react-hook-form";
import { Loader2, MapPin, Sprout, Cloud, Store, Sparkles } from "lucide-react";
import { cn } from "../lib/utils";

const demoProfiles = [
  {
    name: "💰 High Income — Sugarcane, Maharashtra",
    land_size: "15",
    irrigated_percentage: 95,
    soil_type: "Black Cotton",
    crop_type: "Sugarcane",
    season: "Kharif",
    yield_per_acre: "38",
    rainfall: "800",
    temperature: "30",
    market_price: "3500",
    market_distance: "5",
  },
  {
    name: "📉 Low Income — Small Rainfed Plot, Bihar",
    land_size: "1.5",
    irrigated_percentage: 10,
    soil_type: "Sandy",
    crop_type: "Pulses",
    season: "Rabi",
    yield_per_acre: "6",
    rainfall: "400",
    temperature: "25",
    market_price: "4200",
    market_distance: "35",
  },
  {
    name: "🌊 Edge — Flood-Prone Rice, Tamil Nadu",
    land_size: "5",
    irrigated_percentage: 70,
    soil_type: "Alluvial",
    crop_type: "Rice",
    season: "Kharif",
    yield_per_acre: "20",
    rainfall: "1400",
    temperature: "29",
    market_price: "2100",
    market_distance: "12",
  },
  {
    name: "🏔️ Edge — High Yield but Remote, Himachal",
    land_size: "8",
    irrigated_percentage: 50,
    soil_type: "Loamy",
    crop_type: "Vegetables",
    season: "Zaid",
    yield_per_acre: "30",
    rainfall: "650",
    temperature: "18",
    market_price: "6000",
    market_distance: "55",
  },
];

const soilTypes = [
  "Loamy",
  "Clay",
  "Sandy",
  "Black Cotton",
  "Red",
  "Alluvial",
  "Laterite",
];
const cropTypes = [
  "Rice",
  "Wheat",
  "Sugarcane",
  "Cotton",
  "Maize",
  "Soybean",
  "Pulses",
  "Groundnut",
  "Vegetables",
];
const seasons = ["Kharif", "Rabi", "Zaid"];

function InputField({ label, tooltip, error, children }) {
  return (
    <div className="space-y-1.5">
      <label className="flex items-center gap-1 text-sm font-medium text-gray-700">
        {label}
        {tooltip && (
          <span className="group relative">
            <span className="w-4 h-4 rounded-full bg-gray-200 text-gray-500 text-[10px] font-bold inline-flex items-center justify-center cursor-help">
              ?
            </span>
            <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-800 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-10">
              {tooltip}
            </span>
          </span>
        )}
      </label>
      {children}
      {error && <p className="text-xs text-red-500">{error.message}</p>}
    </div>
  );
}

function SectionHeader({ icon: Icon, title }) {
  return (
    <div className="flex items-center gap-2 mb-4 pb-2 border-b border-gray-100">
      <div className="w-7 h-7 rounded-lg bg-primary-100 flex items-center justify-center">
        <Icon className="w-4 h-4 text-primary-600" />
      </div>
      <h3 className="text-sm font-semibold text-gray-800">{title}</h3>
    </div>
  );
}

const inputClass =
  "w-full px-3.5 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-500 transition-all placeholder:text-gray-400";
const selectClass = cn(inputClass, "appearance-none cursor-pointer");

export default function PredictionForm({ onSubmit, isLoading }) {
  const [demoIndex, setDemoIndex] = useState(0);
  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors },
  } = useForm({
    defaultValues: {
      land_size: "",
      irrigated_percentage: 50,
      soil_type: "",
      crop_type: "",
      season: "",
      yield_per_acre: "",
      rainfall: "",
      temperature: "",
      market_price: "",
      market_distance: "",
    },
  });

  const irrigated = watch("irrigated_percentage");

  const fillDemo = () => {
    const profile = demoProfiles[demoIndex];
    const { name: _Name, ...values } = profile;
    reset(values);
    setDemoIndex((prev) => (prev + 1) % demoProfiles.length);
  };

  return (
    <section id="prediction" className="py-16 bg-gray-50/50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-gray-900">
            Income Prediction
          </h2>
          <p className="mt-2 text-gray-500">
            Enter farmer details to predict annual income
          </p>
          <button
            type="button"
            onClick={fillDemo}
            className="mt-4 inline-flex items-center gap-2 bg-primary-50 text-primary-700 px-5 py-2.5 rounded-xl text-sm font-semibold border border-primary-200 hover:bg-primary-100 hover:border-primary-300 transition-all hover:-translate-y-0.5"
          >
            <Sparkles className="w-4 h-4" />
            Try Demo Data — {demoProfiles[demoIndex].name}
          </button>
        </div>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="bg-white rounded-2xl shadow-lg shadow-gray-200/50 border border-gray-100 p-6 sm:p-8"
        >
          {/* Section 1: Farmer & Land */}
          <SectionHeader icon={MapPin} title="Farmer & Land Details" />
          <div className="grid sm:grid-cols-3 gap-4 mb-8">
            <InputField
              label="Land Size (acres)"
              tooltip="Total agricultural land area"
              error={errors.land_size}
            >
              <input
                type="number"
                step="0.1"
                placeholder="e.g. 5.5"
                className={inputClass}
                {...register("land_size", {
                  required: "Required",
                  min: { value: 0.1, message: "Min 0.1" },
                })}
              />
            </InputField>

            <InputField
              label={`Irrigated Land (${irrigated}%)`}
              tooltip="Percentage of land with irrigation"
            >
              <input
                type="range"
                min="0"
                max="100"
                className="w-full accent-primary-600 mt-2"
                {...register("irrigated_percentage")}
              />
            </InputField>

            <InputField
              label="Soil Type"
              tooltip="Dominant soil type in the area"
              error={errors.soil_type}
            >
              <select
                className={selectClass}
                {...register("soil_type", { required: "Select soil type" })}
              >
                <option value="">Select...</option>
                {soilTypes.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </InputField>
          </div>

          {/* Section 2: Crop Details */}
          <SectionHeader icon={Sprout} title="Crop Details" />
          <div className="grid sm:grid-cols-3 gap-4 mb-8">
            <InputField
              label="Crop Type"
              tooltip="Primary crop grown"
              error={errors.crop_type}
            >
              <select
                className={selectClass}
                {...register("crop_type", { required: "Select crop" })}
              >
                <option value="">Select...</option>
                {cropTypes.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </InputField>

            <InputField
              label="Season"
              tooltip="Growing season"
              error={errors.season}
            >
              <select
                className={selectClass}
                {...register("season", { required: "Select season" })}
              >
                <option value="">Select...</option>
                {seasons.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </InputField>

            <InputField
              label="Yield per Acre (quintals)"
              tooltip="Expected crop yield"
              error={errors.yield_per_acre}
            >
              <input
                type="number"
                step="0.1"
                placeholder="e.g. 18"
                className={inputClass}
                {...register("yield_per_acre", {
                  required: "Required",
                  min: { value: 0.1, message: "Min 0.1" },
                })}
              />
            </InputField>
          </div>

          {/* Section 3: Environmental */}
          <SectionHeader icon={Cloud} title="Environmental Conditions" />
          <div className="grid sm:grid-cols-2 gap-4 mb-8">
            <InputField
              label="Rainfall (mm)"
              tooltip="Seasonal average rainfall"
              error={errors.rainfall}
            >
              <input
                type="number"
                placeholder="e.g. 850"
                className={inputClass}
                {...register("rainfall", {
                  required: "Required",
                  min: { value: 0, message: "Min 0" },
                })}
              />
            </InputField>

            <InputField
              label="Temperature (°C)"
              tooltip="Average temperature"
              error={errors.temperature}
            >
              <input
                type="number"
                step="0.1"
                placeholder="e.g. 28.5"
                className={inputClass}
                {...register("temperature", { required: "Required" })}
              />
            </InputField>
          </div>

          {/* Section 4: Market */}
          <SectionHeader icon={Store} title="Market Details" />
          <div className="grid sm:grid-cols-2 gap-4 mb-8">
            <InputField
              label="Price per Quintal (₹)"
              tooltip="Current market selling price"
              error={errors.market_price}
            >
              <input
                type="number"
                placeholder="e.g. 2200"
                className={inputClass}
                {...register("market_price", {
                  required: "Required",
                  min: { value: 1, message: "Min 1" },
                })}
              />
            </InputField>

            <InputField
              label="Distance to Market (km)"
              tooltip="Distance to nearest mandi"
              error={errors.market_distance}
            >
              <input
                type="number"
                step="0.1"
                placeholder="e.g. 12"
                className={inputClass}
                {...register("market_distance", {
                  required: "Required",
                  min: { value: 0, message: "Min 0" },
                })}
              />
            </InputField>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 bg-primary-600 text-white font-semibold rounded-xl hover:bg-primary-700 shadow-lg shadow-primary-600/25 transition-all hover:-translate-y-0.5 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0 flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Predicting...
              </>
            ) : (
              "Predict Income"
            )}
          </button>
        </form>
      </div>
    </section>
  );
}
