

import os
import json
import numpy as np
import pandas as pd
import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Paths ───────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "models")
DEFAULTS_PATH = os.path.join(MODEL_DIR, "feature_defaults.json")

# ── Load models + defaults at startup ───────────────────────
print("Loading models...")
models = []
for i in range(1, 6):
    path = os.path.join(MODEL_DIR, f"lgb_fold{i}.pkl")
    models.append(joblib.load(path))
    print(f"  - Fold {i} loaded")

feature_names = models[0].feature_name()
print(f"  - {len(feature_names)} features expected")

with open(DEFAULTS_PATH) as f:
    feature_defaults = json.load(f)
print(f"  - Defaults loaded for {len(feature_defaults)} features")

# ── App ─────────────────────────────────────────────────────
app = FastAPI(title="AgriPredict AI", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request schema ──────────────────────────────────────────
class PredictionRequest(BaseModel):
    land_size: float = 5.0
    irrigated_percentage: float = 50.0
    soil_type: str = "Loamy"
    crop_type: str = "Rice"
    season: str = "Kharif"
    yield_per_acre: float = 18.0
    rainfall: float = 800.0
    temperature: float = 28.0
    market_price: float = 2200.0
    market_distance: float = 12.0


# ── Feature mapping ────────────────────────────────────────
def build_feature_vector(req: PredictionRequest) -> pd.DataFrame:
    """Map 10 user inputs → 286-feature vector using training medians as defaults."""

    # Start from median defaults
    row = {feat: feature_defaults.get(feat, 0.0) for feat in feature_names}

    # ── Dynamic Prosperity Scaling ──
    # Adjust defaults based on the "richness" of the input profile.
    
    # factors: bigger land, higher yield, higher price, more irrigation = wealthier
    f_land = min(req.land_size / 5.0, 3.0)       # 5 acres = neutral
    f_yield = min(req.yield_per_acre / 20.0, 2.0)
    f_irrig = 0.5 + (req.irrigated_percentage / 100.0)
    f_price = min(req.market_price / 2500.0, 2.0)
    
    prosperity_score = f_land * f_yield * f_irrig * f_price
    
    # Scale specific wealth-related features
    wealth_features = [
        "Non_Agriculture_Income",
        "Avg_Disbursement_Amount_Bureau",
        "No_of_Active_Loan_In_Bureau",
        "Households_with_improved_Sanitation_Facility",
        "perc_of_pop_living_in_hh_electricity",
        "perc_Households_with_Pucca_House_That_Has_More_Than_3_Rooms",
        "Perc_of_house_with_6plus_room",
        "mat_roof_Metal_GI_Asbestos_sheets",
        "perc_of_Wall_material_with_Burnt_brick",
        "Infrastructure_Score",
        "Market_Access_Score",
        "State_Avg_Non_Agriculture_Income",
        "State_Avg_Total_Land_For_Agriculture",
        "K021_Seasonal_Average_Rainfall_mm", # sometimes rain implies better region
    ]
    
    for feat in wealth_features:
        if feat in row:
            # Stronger scaling: square the prosperity score to punish low values more
            # e.g. 0.3 becomes 0.09
            multiplier = getattr(req, "land_size", 5) / 5.0 if feat == "State_Avg_Total_Land_For_Agriculture" else prosperity_score
            multiplier = max(0.05, min(multiplier, 3.0)) # Floor at 5% instead of 30%
            
            if req.land_size < 2.0:
                 multiplier *= 0.1 # CRUSH wealth for very small farmers

            row[feat] = row[feat] * multiplier

    # Specific overrides
    if req.land_size < 2.0:
        row["KCC_Access"] = 0
        row["No_of_Active_Loan_In_Bureau"] = 0
        row["Avg_Disbursement_Amount_Bureau"] = 0
        row["Non_Agriculture_Income"] = 0
        row["State_Avg_Non_Agriculture_Income"] *= 0.1
    
    # --- Direct mappings ---
    row["Total_Land_For_Agriculture"] = req.land_size
    row["Non_Agriculture_Income"] = row["Non_Agriculture_Income"]
    row["K022_Proximity_to_nearest_mandi_Km"] = req.market_distance
    row["K022_Net_Agri_area_in_Ha"] = req.land_size * 0.4047

    # ... (Temperature/Rainfall mappings same as before) ...
    for prefix in ["K021", "K022", "R020", "R021", "R022"]:
         if f"{prefix}_Ambient_temperature_min_max__max" in row:
             row[f"{prefix}_Ambient_temperature_min_max__max"] = req.temperature + 5
         if f"{prefix}_Ambient_temperature_min_max__min" in row:
             row[f"{prefix}_Ambient_temperature_min_max__min"] = req.temperature - 5
         if f"{prefix}_Ambient_temperature_min_max__range" in row:
             row[f"{prefix}_Ambient_temperature_min_max__range"] = 10
 
    # Rainfall (map to all seasonal rainfall features)
    for prefix in ["K021", "K022", "R020", "R021", "R022"]:
         key = f"{prefix}_Seasonal_Average_Rainfall_mm"
         if key in row:
             row[key] = req.rainfall

    # Irrigation (Kharif + Rabi irrigated area features)
    irr_fraction = req.irrigated_percentage / 100.0
    irr_area = req.land_size * 0.4047 * irr_fraction
    for col in feature_names:
        if "Irrigated_area" in col:
            row[col] = irr_area

    # Agricultural scores (higher irrigation = better score)
    agri_score = 50 + irr_fraction * 30 + min(req.yield_per_acre, 30) / 30 * 20
    for col in feature_names:
        if "Agricultural_Score" in col:
            row[col] = agri_score
        elif "Agricultural_performance" in col:
            row[col] = min(agri_score / 20, 5)  # 1-5 scale

    # Cropping density (higher yield = denser cropping)
    crop_density = min(req.yield_per_acre / 20, 2.0)
    for col in feature_names:
        if "Cropping_density" in col:
            row[col] = crop_density

    # Engineered features
    row["Land_sq"] = req.land_size ** 2
    row["NonAgriIncome_sq"] = row["Non_Agriculture_Income"] ** 2  # Sync!
    row["Land_per_Person"] = req.land_size / 4
    row["Income_x_Land"] = row["Non_Agriculture_Income"] * req.land_size # Approximation
    row["Loan_to_Income_Ratio"] = (row["Avg_Disbursement_Amount_Bureau"] / (row["Non_Agriculture_Income"] + 1)) if row["Avg_Disbursement_Amount_Bureau"] > 0 else 0
    # Temperature (map to all seasonal temp features)
    for prefix in ["K021", "K022", "R020", "R021", "R022"]:
        if f"{prefix}_Ambient_temperature_min_max__max" in row:
            row[f"{prefix}_Ambient_temperature_min_max__max"] = req.temperature + 5
        if f"{prefix}_Ambient_temperature_min_max__min" in row:
            row[f"{prefix}_Ambient_temperature_min_max__min"] = req.temperature - 5
        if f"{prefix}_Ambient_temperature_min_max__range" in row:
            row[f"{prefix}_Ambient_temperature_min_max__range"] = 10

    # Rainfall (map to all seasonal rainfall features)
    for prefix in ["K021", "K022", "R020", "R021", "R022"]:
        key = f"{prefix}_Seasonal_Average_Rainfall_mm"
        if key in row:
            row[key] = req.rainfall

    # Irrigation (Kharif + Rabi irrigated area features)
    irr_fraction = req.irrigated_percentage / 100.0
    irr_area = req.land_size * 0.4047 * irr_fraction
    for col in feature_names:
        if "Irrigated_area" in col:
            row[col] = irr_area

    # Agricultural scores (higher irrigation = better score)
    agri_score = 50 + irr_fraction * 30 + min(req.yield_per_acre, 30) / 30 * 20
    for col in feature_names:
        if "Agricultural_Score" in col:
            row[col] = agri_score
        elif "Agricultural_performance" in col:
            row[col] = min(agri_score / 20, 5)  # 1-5 scale

    # Cropping density (higher yield = denser cropping)
    crop_density = min(req.yield_per_acre / 20, 2.0)
    for col in feature_names:
        if "Cropping_density" in col:
            row[col] = crop_density

    # Sex — use median (0 or 1)
    # Marital status — use median

    # Engineered features
    row["Land_sq"] = req.land_size ** 2
    row["NonAgriIncome_sq"] = 0
    row["Land_per_Person"] = req.land_size / 4  # assume 4-person household
    row["Income_x_Land"] = 0  # can't compute without target
    row["Loan_to_Income_Ratio"] = 0

    # Rainfall aggregates
    row["Rainfall_Mean"] = req.rainfall
    row["Rainfall_Trend"] = 0
    row["Rainfall_Variability"] = req.rainfall * 0.1

    # Agri trend (Kharif vs Rabi)
    row["Agri_Trend_Kharif"] = 0
    row["Agri_Trend_Rabi"] = 0
    row["Avg_Agri_Score"] = agri_score

    # Infrastructure & market scores
    row["Infrastructure_Score"] = 50 + irr_fraction * 30
    row["Market_Access_Score"] = max(0, 100 - req.market_distance * 2)
    row["KCC_Access"] = 1 if req.land_size > 2 else 0

    # Socio-economic (use reasonable defaults)
    row["Land_x_SocioScore"] = req.land_size * 50
    row["SocioScore_x_MandiDist"] = 50 * req.market_distance

    # Land holding index
    if "Land_Holding_Index_source_Total_Agri_Area_no_of_people" in row:
        row["Land_Holding_Index_source_Total_Agri_Area_no_of_people"] = req.land_size / 4

    # Build DataFrame
    df = pd.DataFrame([row], columns=feature_names)
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)
    return df


# ── Endpoints ───────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "models_loaded": len(models), "features": len(feature_names)}


@app.post("/api/predict")
def predict(req: PredictionRequest):
    print(f"Received prediction request: {req}")

    # Build feature vector
    X = build_feature_vector(req)

    # Predict with all 5 fold models and average (log scale)
    preds_log = []
    for model in models:
        pred = model.predict(X, num_iteration=model.best_iteration)[0]
        preds_log.append(pred)

    avg_log = np.mean(preds_log)

    # Inverse log transform → real income
    predicted_income = int(np.expm1(avg_log))
    
    # ── Post-processing Heuristic ──
    f_land = min(req.land_size / 5.0, 3.0)
    f_yield = min(req.yield_per_acre / 20.0, 2.0)
    f_irrig = 0.5 + (req.irrigated_percentage / 100.0)
    f_price = min(req.market_price / 2500.0, 2.0)
    prosperity = f_land * f_yield * f_irrig * f_price
    
    # 1. Dampen huge predictions for remote farms (market distance > 20km)
    if req.market_distance > 20:
        penalty = min(req.market_distance / 100.0, 0.4) # up to 40% penalty
        predicted_income = int(predicted_income * (1.0 - penalty))

    # 2. If very poor profile, dampen the regression-to-mean effect
    if prosperity < 0.4:
         predicted_income = int(predicted_income * (0.5 + prosperity))
    
    predicted_income = max(predicted_income, 15000)

    # Loan eligibility
    if predicted_income >= 800000:
        loan_eligibility = "High"
    elif predicted_income >= 350000:
        loan_eligibility = "Medium"
    else:
        loan_eligibility = "Low"

    return {
        "predicted_income": predicted_income,
        "loan_eligibility": loan_eligibility,
        "model_version": "v2.0-lightgbm",
        "features_used": len(feature_names),
        "fold_predictions": [int(np.expm1(p)) for p in preds_log],
    }


# ── Run ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
