import pandas as pd
import xgboost as xgb
import catboost as cb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
import re

# Load the cleaned data
df = pd.read_csv('TrainData_cleaned.csv', low_memory=False)

# Clean column names
df.columns = [re.sub(r'[^A-Za-z0-9_]+', '_', col) for col in df.columns]

# Select features
features = [
    'No_of_Active_Loan_In_Bureau',
    'Avg_Disbursement_Amount_Bureau',
    'Non_Agriculture_Income',
    'Total_Land_For_Agriculture',
    'Village_Population',
    'K022_Proximity_to_nearest_mandi_Km_',
    'K022_Proximity_to_nearest_railway_Km_',
    'KO22_Village_score_based_on_socio_economic_parameters_0_to_100_',
    'Night_light_index',
    'Road_density_Km_SqKm_'
]

target = 'Target_Variable_Total_Income'

# Add the one-hot encoded columns to the features list
for col in df.columns:
    if col.startswith('Kharif_Seasons_Type_of_soil_in_2020') or \
       col.startswith('Rabi_Seasons_Type_of_soil_in_2020') or \
       col.startswith('Kharif_Seasons_Type_of_water_bodies_in_hectares_2020') or \
       col.startswith('Rabi_Seasons_Type_of_water_bodies_in_hectares_2020'):
        features.append(col)

X = df[features]
y = df[target]

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost model
print("Training XGBoost model...")
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000, learning_rate=0.05, n_jobs=-1, random_state=42)
xgb_model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False)

# Evaluate XGBoost model
xgb_preds = xgb_model.predict(X_val)
xgb_mape = mean_absolute_percentage_error(y_val, xgb_preds)
print(f"XGBoost MAPE: {xgb_mape}")

# Train CatBoost model
print("Training CatBoost model...")
cb_model = cb.CatBoostRegressor(iterations=1000, learning_rate=0.05, random_seed=42, verbose=0)
cb_model.fit(X_train, y_train, eval_set=(X_val, y_val), early_stopping_rounds=100)

# Evaluate CatBoost model
cb_preds = cb_model.predict(X_val)
cb_mape = mean_absolute_percentage_error(y_val, cb_preds)
print(f"CatBoost MAPE: {cb_mape}")
