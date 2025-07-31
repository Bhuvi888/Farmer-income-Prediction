import pandas as pd
import numpy as np
import re
import os

script_dir = os.path.dirname(__file__)

def create_seasonal_interaction_features(df_train, df_test):
    # Identify one-hot encoded columns for Kharif and Rabi soil and water bodies
    kharif_soil_cols = [col for col in df_train.columns if col.startswith('Kharif_Seasons_Type_of_soil_in_2020_')]
    rabi_soil_cols = [col for col in df_train.columns if col.startswith('Rabi_Seasons_Type_of_soil_in_2020_')]
    kharif_water_cols = [col for col in df_train.columns if col.startswith('Kharif_Seasons_Type_of_water_bodies_in_hectares_2020_')]
    rabi_water_cols = [col for col in df_train.columns if col.startswith('Rabi_Seasons_Type_of_water_bodies_in_hectares_2020_')]

    # Create interaction features for soil types
    for k_col in kharif_soil_cols:
        # Extract the soil type from the column name
        soil_type = k_col.replace('Kharif_Seasons_Type_of_soil_in_2020_', '')
        r_col = f'Rabi_Seasons_Type_of_soil_in_2020_{soil_type}'
        if r_col in rabi_soil_cols:
            df_train[f'Soil_Interaction_{soil_type}'] = df_train[k_col] * df_train[r_col]
            df_test[f'Soil_Interaction_{soil_type}'] = df_test[k_col] * df_test[r_col]

    # Create interaction features for water body types
    for k_col in kharif_water_cols:
        # Extract the water body type from the column name
        water_type = k_col.replace('Kharif_Seasons_Type_of_water_bodies_in_hectares_2020_', '')
        r_col = f'Rabi_Seasons_Type_of_water_bodies_in_hectares_2020_{water_type}'
        if r_col in rabi_water_cols:
            df_train[f'Water_Interaction_{water_type}'] = df_train[k_col] * df_train[r_col]
            df_test[f'Water_Interaction_{water_type}'] = df_test[k_col] * df_test[r_col]

    return df_train, df_test

if __name__ == "__main__":
    # Load cleaned data with geographical features
    try:
        train_df = pd.read_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TrainData_geo_fe.csv')), low_memory=False)
        test_df = pd.read_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TestData_geo_fe.csv')), low_memory=False)
        print("Cleaned data with geographical features loaded successfully.")
    except FileNotFoundError:
        print("Error: Cleaned data files not found. Please run data_cleaning.py, preprocess_test_data.py, and feature_engineering_geo.py first.")
        exit()

    # Clean column names for consistency (from data_cleaning.py and eda.py)
    

    # Align columns before creating interaction features
    common_cols = list(set(train_df.columns) | set(test_df.columns))
    train_df = train_df.reindex(columns=common_cols, fill_value=0)
    test_df = test_df.reindex(columns=common_cols, fill_value=0)

    # Apply seasonal interaction feature engineering
    train_df_fe, test_df_fe = create_seasonal_interaction_features(train_df, test_df)

    # Save the data with new features
    train_df_fe.to_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TrainData_seasonal_fe.csv')), index=False)
    test_df_fe.to_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TestData_seasonal_fe.csv')), index=False)
    print("Seasonal interaction features engineered and saved to TrainData_seasonal_fe.csv and TestData_seasonal_fe.csv")
