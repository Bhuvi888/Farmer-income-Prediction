import pandas as pd
import numpy as np
import re
import os

# Get the path of the current script (src/)
script_dir = os.path.dirname(__file__)

# Define the path to your CSV file
file_path = os.path.abspath(os.path.join(script_dir, '..', 'data', 'raw', 'TestData.csv'))

try:
    # Read the CSV file into a pandas DataFrame
    print("Loading test data from CSV...")
    df = pd.read_csv(file_path, low_memory=False)
    print("Test data loaded successfully.")

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    print("Stripped whitespace from column names.")

    # Handle missing values in 'Avg_Disbursement_Amount_Bureau'
    # For now, we'll fill missing values with the mean. (Using 0 for test data as mean from train data is not available here)
    # In a real scenario, you would use the mean from the training data.
    if 'Avg_Disbursement_Amount_Bureau' in df.columns:
        df['Avg_Disbursement_Amount_Bureau'].fillna(0, inplace=True)
    print("Missing values in 'Avg_Disbursement_Amount_Bureau' handled.")

    # Apply log transformation to skewed columns
    for col in ['No_of_Active_Loan_In_Bureau', 'Non_Agriculture_Income']:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: np.log1p(x))
    print("Log transformation applied to skewed columns.")

    # Create Village_Population feature
    if 'VILLAGE' in df.columns:
        df['Village_Population'] = df['VILLAGE'].map(df['VILLAGE'].value_counts())
        df['Village_Population'].fillna(0, inplace=True) # Handle villages not in training data
    else:
        df['Village_Population'] = 0 # If VILLAGE column is missing
    print("Created Village_Population feature.")

    # One-hot encode categorical features for 2020
    for col in ['Kharif Seasons Type of soil in 2020', 'Rabi Seasons Type of soil in 2020', 'Kharif Seasons Type of water bodies in hectares 2020', 'Rabi Seasons Type of water bodies in hectares 2020']:
        if col in df.columns:
            # Get dummy variables and concatenate
            dummies = pd.get_dummies(df[col], prefix=col, dummy_na=True)
            df = pd.concat([df, dummies], axis=1)
            df.drop(columns=[col], inplace=True)
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
    if 'Total_Land_For_Agriculture' in df.columns and 'KO22-Village score based on socio-economic parameters (0 to 100)' in df.columns:
        df['Land_x_SocioEconomicScore'] = df['Total_Land_For_Agriculture'] * df['KO22-Village score based on socio-economic parameters (0 to 100)']
    else:
        df['Land_x_SocioEconomicScore'] = 0 # Default value if columns are missing

    if 'Total_Land_For_Agriculture' in df.columns and 'Village_Population' in df.columns and (df['Village_Population'] != 0).any():
        df['Land_per_Person'] = df['Total_Land_For_Agriculture'] / df['Village_Population']
    else:
        df['Land_per_Person'] = 0 # Default value if columns are missing or Village_Population is zero
    print("Created interaction features.")

    # Save the cleaned data
    output_path = os.path.abspath(os.path.join(script_dir, '..', 'data', 'TestData_cleaned.csv'))
    df.to_csv(output_path, index=False)
    print("Cleaned test data saved to TestData_cleaned.csv")

except FileNotFoundError:
    print(f"Error: The file {file_path} was not found at the specified path.")
except Exception as e:
    print(f"An error occurred: {e}")
