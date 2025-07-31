import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error
import re
import joblib
import os

script_dir = os.path.dirname(__file__)

# Load the cleaned data
df = pd.read_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TrainData_seasonal_fe.csv')), low_memory=False)

# Clean column names for LightGBM
df.columns = [re.sub(r'[^A-Za-z0-9_]+', '_', col) for col in df.columns]
print("Cleaned column names.")

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

features.extend(['Land_x_SocioEconomicScore', 'Land_per_Person', 'State_Encoded', 'VILLAGE_Encoded'])

# Add the one-hot encoded columns to the features list
for col in df.columns:
    if col.startswith('Kharif_Seasons_Type_of_soil_in_2020') or \
       col.startswith('Rabi_Seasons_Type_of_soil_in_2020') or \
       col.startswith('Kharif_Seasons_Type_of_water_bodies_in_hectares_2020') or \
       col.startswith('Rabi_Seasons_Type_of_water_bodies_in_hectares_2020') or \
       col.endswith('_min') or col.endswith('_max') or col.endswith('_range') or \
       col.startswith('Soil_Interaction_') or col.startswith('Water_Interaction_'):
        features.append(col)


X = df[features]
y = df[target]

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train LightGBM model
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_val, y_val, reference=lgb_train)

params = {
    'objective': 'regression_l1',
    'metric': 'mape',
    'n_estimators': 1000,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': -1,
    'n_jobs': -1,
    'seed': 42
}

print("Training LightGBM model...")
model = lgb.train(params,
                lgb_train,
                num_boost_round=1000,
                valid_sets=[lgb_train, lgb_eval],
                callbacks=[lgb.early_stopping(100, verbose=True)])

# Evaluate model
preds = model.predict(X_val, num_iteration=model.best_iteration)
mape = mean_absolute_percentage_error(y_val, preds)
print(f"MAPE: {mape}")

joblib.dump(model, os.path.abspath(os.path.join(script_dir, '..', 'models', 'best_lightgbm_model.pkl')))
print("Best LightGBM model saved as ../models/best_lightgbm_model.pkl")