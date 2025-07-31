import pandas as pd
import numpy as np
import re

# Load the training data
try:
    df = pd.read_csv('data/raw/LTF_Challenge_TrainData.csv', low_memory=False)
    print("Training data loaded successfully.")
except FileNotFoundError:
    print("Error: data/raw/LTF_Challenge_TrainData.csv not found. Please ensure the file is in the correct location.")
    exit()

# Strip whitespace from column names
df.columns = df.columns.str.strip()
print("Stripped whitespace from column names.")

# Handle missing values in 'Avg_Disbursement_Amount_Bureau'
# For now, we'll fill missing values with the mean.
mean_disbursement = df['Avg_Disbursement_Amount_Bureau'].mean()
df['Avg_Disbursement_Amount_Bureau'].fillna(mean_disbursement, inplace=True)

print("Missing values in 'Avg_Disbursement_Amount_Bureau' handled.")

# Apply log transformation to skewed columns
for col in ['No_of_Active_Loan_In_Bureau', 'Non_Agriculture_Income', 'Target_Variable/Total Income']:
    df[col] = df[col].apply(lambda x: np.log1p(x))

print("Log transformation applied to skewed columns.")

# Create Village_Population feature
df['Village_Population'] = df['VILLAGE'].map(df['VILLAGE'].value_counts())

print("Created Village_Population feature.")

# One-hot encode categorical features for 2020
for col in ['Kharif Seasons Type of soil in 2020', 'Rabi Seasons Type of soil in 2020', 'Kharif Seasons Type of water bodies in hectares 2020', 'Rabi Seasons Type of water bodies in hectares 2020']:
    df = pd.get_dummies(df, columns=[col], dummy_na=True)

print("One-hot encoded categorical features for 2020.")

# Create temperature features
for col in ['K022-Ambient temperature (min & max)', 'R022-Ambient temperature (min & max)', 'K021-Ambient temperature (min & max)', 'R021-Ambient temperature (min & max)', 'R020-Ambient temperature (min & max)']:
    if col in df.columns:
        df[col] = df[col].astype(str)
        # Handle different separators ('&' or '/')
        temp_splits = df[col].apply(lambda x: re.split(r'\s*&\s*|\s*/\s*', x))
        df[col + '_min'] = temp_splits.apply(lambda x: x[0] if len(x) > 0 else None).astype(float)
        df[col + '_max'] = temp_splits.apply(lambda x: x[1] if len(x) > 1 else None).astype(float)
        df[col + '_range'] = df[col + '_max'] - df[col + '_min']
        df.drop(columns=[col], inplace=True)

print("Created temperature features.")

# Create interaction features
df['Land_x_SocioEconomicScore'] = df['Total_Land_For_Agriculture'] * df['KO22-Village score based on socio-economic parameters (0 to 100)']
df['Land_per_Person'] = df['Total_Land_For_Agriculture'] / df['Village_Population']

print("Created interaction features.")

# Save the cleaned data
df.to_csv('data/TrainData_cleaned.csv', index=False)
print("Cleaned data saved to data/TrainData_cleaned.csv")