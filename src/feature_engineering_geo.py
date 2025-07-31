import pandas as pd
import numpy as np
import os

def create_geographical_features(df_train, df_test):
    # Target Encoding for 'State'
    state_income_map = df_train.groupby('State')['Target_Variable/Total Income'].mean().to_dict()
    df_train['State_Encoded'] = df_train['State'].map(state_income_map)
    df_test['State_Encoded'] = df_test['State'].map(state_income_map)
    # Fill NaN values in test set (for states not seen in training) with the overall mean
    overall_mean_income = df_train['Target_Variable/Total Income'].mean()
    df_test['State_Encoded'].fillna(overall_mean_income, inplace=True)

    # Target Encoding for 'VILLAGE'
    village_income_map = df_train.groupby('VILLAGE')['Target_Variable/Total Income'].mean().to_dict()
    df_train['VILLAGE_Encoded'] = df_train['VILLAGE'].map(village_income_map)
    df_test['VILLAGE_Encoded'] = df_test['VILLAGE'].map(village_income_map)
    # Fill NaN values in test set (for villages not seen in training) with the overall mean
    df_test['VILLAGE_Encoded'].fillna(overall_mean_income, inplace=True)

    return df_train, df_test

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    # Load cleaned data
    try:
        train_df = pd.read_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TrainData_cleaned.csv')), low_memory=False)
        test_df = pd.read_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TestData_cleaned.csv')), low_memory=False)
        print("Cleaned data loaded successfully.")
    except FileNotFoundError:
        print("Error: Cleaned data files not found. Please run data_cleaning.py and preprocess_test_data.py first.")
        exit()

    # Apply geographical feature engineering
    train_df_fe, test_df_fe = create_geographical_features(train_df.copy(), test_df.copy())

    # Save the data with new features
    train_df_fe.to_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TrainData_geo_fe.csv')), index=False)
    test_df_fe.to_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TestData_geo_fe.csv')), index=False)
    print("Geographical features engineered and saved to TrainData_geo_fe.csv and TestData_geo_fe.csv")
