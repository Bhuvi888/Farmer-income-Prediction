# Model Documentation: Farmer Income Prediction

## 1. Introduction

This document outlines the machine learning pipeline developed for predicting farmer income, a crucial factor in assessing creditworthiness. The primary goal is to build a robust predictive model, with Mean Absolute Percentage Error (MAPE) as the key evaluation metric.

## 2. Pipeline Overview

The predictive pipeline is structured into several sequential stages:

1.  **Data Cleaning & Preprocessing:** Initial preparation of raw data.
2.  **Feature Engineering:** Creation of new, more informative features from existing ones.
3.  **Model Training & Evaluation:** Training a LightGBM model and assessing its performance.
4.  **Hyperparameter Tuning:** Optimizing the model's parameters for better performance.
5.  **Prediction Generation:** Generating final income predictions on unseen test data.

## 3. Detailed Pipeline Steps

### 3.1. Data Cleaning & Preprocessing (`src/data_cleaning.py`, `src/preprocess_test_data.py`)

This stage focuses on preparing the raw `TrainData.csv` and `TestData.csv` for modeling.

*   **Data Loading:** Both training and test datasets are loaded.
*   **Column Name Cleaning:** Whitespace is stripped from all column names for consistency and easier access.
*   **Missing Value Handling:** Missing values in `Avg_Disbursement_Amount_Bureau` are imputed. For the training data, they are filled with the mean of the column. For the test data, they are filled with 0 (as the training mean is not available during test data preprocessing).
*   **Log Transformation:** Skewed numerical features (`No_of_Active_Loan_In_Bureau`, `Non_Agriculture_Income`, and `Target_Variable/Total Income` for training data) are log-transformed (`np.log1p`) to reduce skewness and improve model performance.

### 3.2. Feature Engineering (`src/feature_engineering_geo.py`, `src/feature_engineering_seasonal.py`)

This stage involves creating new features to capture more complex relationships within the data.

*   **Village Population:** A `Village_Population` feature is created by counting the number of farmers per village based on the `VILLAGE` column.
*   **Temperature Features:** Ambient temperature columns (e.g., `K022-Ambient temperature (min & max)`) are parsed to extract `_min`, `_max`, and `_range` (max - min) features.
*   **One-Hot Encoding:** Categorical features related to soil type and water bodies for the year 2020 (e.g., `Kharif Seasons Type of soil in 2020`, `Rabi Seasons Type of water bodies in hectares 2020`) are one-hot encoded.
*   **Interaction Features:**
    *   `Land_x_SocioEconomicScore`: An interaction term created by multiplying `Total_Land_For_Agriculture` and `KO22-Village score based on socio-economic parameters (0 to 100)`.
    *   `Land_per_Person`: Calculated as `Total_Land_For_Agriculture` divided by `Village_Population`.
*   **Geographical Features (Target Encoding):**
    *   `State_Encoded`: The `State` column is target-encoded using the mean of `Target_Variable/Total Income` for each state from the training data. Unseen states in the test set are filled with the overall mean income from the training data.
    *   `VILLAGE_Encoded`: Similar to state encoding, the `VILLAGE` column is target-encoded using the mean of `Target_Variable/Total Income` for each village from the training data. Unseen villages in the test set are filled with the overall mean income from the training data.
*   **Seasonal Interaction Features:** Interaction terms are created by multiplying corresponding one-hot encoded soil types (e.g., `Kharif_Soil_TypeX * Rabi_Soil_TypeX`) and water body types across Kharif and Rabi seasons. This aims to capture the combined effect of these seasonal characteristics.

### 3.3. Model Training & Evaluation (`src/train_lightgbm.py`)

*   **Model Choice:** LightGBM (Light Gradient Boosting Machine) is chosen as the primary model due to its efficiency and performance in tabular data tasks.
*   **Evaluation Metric:** MAPE (Mean Absolute Percentage Error) is used to evaluate model performance, aligning with the project's objective.
*   **Training Process:** The data is split into training and validation sets (80/20 split). The LightGBM model is trained on the training set, and its performance is monitored on the validation set using early stopping to prevent overfitting.

### 3.4. Hyperparameter Tuning (`src/tune_lightgbm.py`)

*   **Methodology:** Randomized Search Cross-Validation (`RandomizedSearchCV`) is employed to efficiently search for the optimal combination of LightGBM hyperparameters.
*   **Objective:** The tuning aims to minimize MAPE on the validation sets.
*   **Output:** The best-performing model from the tuning process is saved as `models/best_lightgbm_model.pkl`.

### 3.5. Prediction Generation (`src/predict_test_data.py`)

*   **Test Data Transformation:** The same data cleaning and feature engineering steps applied to the training data are applied to the `TestData.csv` to ensure consistency.
*   **Model Loading:** The saved `best_lightgbm_model.pkl` is loaded.
*   **Prediction:** Predictions are generated on the preprocessed test data. Since the target variable was log-transformed, the predictions are inverse-transformed (`np.expm1`) to get the actual income values.
*   **Output:** The final predictions, along with `FarmerID`, are saved to `predictions/Predicted_Farmer_Income.csv`.

## 4. Key Results

After implementing the full pipeline, including geographical and seasonal interaction features, the best LightGBM model achieved a MAPE of approximately **1.436%** on the validation set during hyperparameter tuning. This indicates a strong predictive performance on unseen data from the same distribution as the training data.

## 5. How to Run

For detailed instructions on setting up the environment and running the pipeline, please refer to the `README.md` file in the project's root directory.
