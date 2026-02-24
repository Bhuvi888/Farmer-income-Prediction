# Model Documentation: AgriPredict AI (Farmer Income Prediction V2)

This document outlines the version 2.0 machine learning pipeline and system architecture developed for predicting farmer income to assess creditworthiness.

## 1. System Architecture

The project has evolved into a full-stack AI application:

- **ML Engine (Python/LightGBM):** High-precision gradient boosting models.
- **Backend (FastAPI):** A high-performance REST API that serves predictions using an ensemble of models.
- **Frontend (React/Vite):** A premium web dashboard with interactive data visualizations (Recharts).

## 2. ML Pipeline Overview (V2)

The pipeline is structured into several modular stages:

1.  **Data Cleaning:** Handling missing values and trimming column whitespace.
2.  **Advanced Feature Engineering:**
    - **Geographical Encoding:** K-Fold Target Encoding for States and Villages to prevent data leakage.
    - **Interaction Terms:** `Land_x_SocioScore`, `Income_x_Land`, `NightLight_x_RoadDensity`.
    - **Ratios:** `Loan_to_Income_Ratio`, `Land_per_Person`, `Market_Access_Score`.
    - **Environmental:** Seasonal rainfall variability and parsed temperature min/max/range.
    - **Trends:** Agricultural performance trends across 2020-2022.
3.  **Modeling (5-Fold Ensemble):**
    - Instead of a single model, we use a 5-fold cross-validation ensemble.
    - **Algorithm:** LightGBM (MAE/MAPE objective).
    - **Stability:** Predictions are averaged across 5 folds to reduce variance.

## 3. Real-time Inference Logic

When a user submits data through the web UI, the backend performs:

- **Median Imputation:** Unprovided features are filled with training-set medians.
- **Prosperity Scaling:** A heuristic that scales wealth-related features (like infrastructure or bureau data) based on the user's input (land size, yield, etc.).
- **Log Correlation Sync:** Ensuring squared features (e.g., `Land_sq`) remain consistent with input changes.
- **Post-processing Heuristics:** Dampening extreme predictions for remote geographical profiles (market distance > 20km).

## 4. Key Performance Metrics

The V2 pipeline achieved significant improvements over the baseline:

- **Baseline MAPE:** 1.68%
- **Optimized V2 OOF MAPE:** ~1.436% (Log-scale)
- **CV Stability:** Validated across 5 folds with low standard deviation.

## 5. Web Features & Visualization

The frontend provides real-time insights:

- **Model Stability Chart:** Visualizes the prediction variance across all 5 ensemble folds.
- **Cost vs Profit Analysis:** Breakdown of seed, fertilizer, labor, and machinery costs relative to predicted income.
- **Loan Eligibility Status:** Automated "High/Medium/Low" classification based on predicted income thresholds.

## 6. How to Run

1.  **Backend:** `cd backend && python main.py` (Runs on port 5000)
2.  **Frontend:** `cd frontend && npm run dev`
3.  **ML Pipeline:** `python run_pipeline_v2.py`
