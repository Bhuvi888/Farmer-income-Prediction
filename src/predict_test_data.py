import pandas as pd
import numpy as np
import joblib
import re
import os

script_dir = os.path.dirname(__file__)

# Load the preprocessed test data
df_test = pd.read_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TestData_seasonal_fe.csv')), low_memory=False)

# Clean column names for consistency with training
original_farmer_ids = df_test['FarmerID']
df_test.columns = [re.sub(r'[^A-Za-z0-9_]+', '_', col) for col in df_test.columns]

# Load the trained LightGBM model
best_model = joblib.load(os.path.abspath(os.path.join(script_dir, '..', 'models', 'best_lightgbm_model.pkl')))

# Ensure test data has the same columns as training data
# Get feature names from the trained model
model_features = best_model.feature_name()

# Align columns - add missing columns with 0 and drop extra ones
missing_cols = set(model_features) - set(df_test.columns)
for c in missing_cols:
    df_test[c] = 0

extra_cols = set(df_test.columns) - set(model_features)
for c in extra_cols:
    df_test.drop(c, axis=1, inplace=True)

df_test = df_test[model_features]

# Make predictions (predictions are log-transformed)
log_predictions = best_model.predict(df_test)

# Inverse transform the predictions to get actual income values
predictions = np.expm1(log_predictions)

# Create a DataFrame for submission
submission_df = pd.DataFrame({'FarmerID': original_farmer_ids, 'Predicted_Income': predictions})

# Save the predictions to a CSV file
submission_df.to_csv(os.path.abspath(os.path.join(script_dir, '..', 'predictions', 'Predicted_Farmer_Income.csv')), index=False)

print("Predictions saved to Predicted_Farmer_Income.csv")
