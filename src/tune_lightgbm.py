import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import mean_absolute_percentage_error, make_scorer
import re
import numpy as np
import os

script_dir = os.path.dirname(__file__)

# Load the cleaned data
df = pd.read_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TrainData_seasonal_fe.csv')), low_memory=False)

# Clean column names for LightGBM
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
    'Road_density_Km_SqKm_',
    'Land_x_SocioEconomicScore',
    'Land_per_Person',
    'State_Encoded',
    'VILLAGE_Encoded'
]

# Add the one-hot encoded columns to the features list
for col in df.columns:
    if col.startswith('Kharif_Seasons_Type_of_soil_in_2020') or \
       col.startswith('Rabi_Seasons_Type_of_soil_in_2020') or \
       col.startswith('Kharif_Seasons_Type_of_water_bodies_in_hectares_2020') or \
       col.startswith('Rabi_Seasons_Type_of_water_bodies_in_hectares_2020') or \
       col.endswith('_min') or col.endswith('_max') or col.endswith('_range') or \
       col.startswith('Soil_Interaction_') or col.startswith('Water_Interaction_'):
        features.append(col)

target = 'Target_Variable_Total_Income'

X = df[features]
y = df[target]

# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the parameter distribution for RandomizedSearchCV
param_dist = {
    'n_estimators': [500, 1000, 1500, 2000],
    'learning_rate': [0.01, 0.05, 0.1],
    'num_leaves': [20, 31, 40, 50],
    'max_depth': [-1, 10, 20],
    'min_child_samples': [20, 30, 40],
    'subsample': [0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
    'reg_alpha': [0, 0.1, 0.5, 1.0],
    'reg_lambda': [0, 0.1, 0.5, 1.0]
}

# Custom MAPE scorer for RandomizedSearchCV
mape_scorer = make_scorer(mean_absolute_percentage_error, greater_is_better=False)

# Initialize LightGBM Regressor
lgb_model = lgb.LGBMRegressor(objective='regression_l1', random_state=42, n_jobs=-1)

# Initialize RandomizedSearchCV
rand_search = RandomizedSearchCV(estimator=lgb_model,
                                 param_distributions=param_dist,
                                 n_iter=50,  # Number of parameter settings that are sampled
                                 scoring=mape_scorer,
                                 cv=3,       # 3-fold cross-validation
                                 verbose=2,
                                 random_state=42,
                                 n_jobs=-1)

print("Starting RandomizedSearchCV...")
rand_search.fit(X_train, y_train)

print("Best parameters found:", rand_search.best_params_)
print("Best MAPE (negative, so lower is better):", rand_search.best_score_)

# Evaluate the best model on the validation set
best_model = rand_search.best_estimator_
preds = best_model.predict(X_val)
mape = mean_absolute_percentage_error(y_val, preds)
print(f"MAPE on validation set with best model: {mape}")

import joblib
joblib.dump(best_model, os.path.abspath(os.path.join(script_dir, '..', 'models', 'best_lightgbm_model.pkl')))