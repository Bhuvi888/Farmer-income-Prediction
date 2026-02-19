"""
Centralized configuration for the Farmer Income Prediction pipeline.
All paths, column definitions, and hyperparameters live here.
"""

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
PRED_DIR = os.path.join(BASE_DIR, "predictions")

TRAIN_RAW = os.path.join(RAW_DIR, "LTF_Challenge_TrainData.csv")
TEST_RAW = os.path.join(RAW_DIR, "TestData.csv")

# ---------------------------------------------------------------------------
# General
# ---------------------------------------------------------------------------
SEED = 42
N_FOLDS = 5
TARGET_COL = "Target_Variable_Total_Income"   # after column-name cleaning
TARGET_COL_RAW = "Target_Variable/Total Income"

# ---------------------------------------------------------------------------
# Column groups (raw names, before cleaning)
# ---------------------------------------------------------------------------

# Columns to drop entirely (IDs, free text, duplicates)
DROP_COLS = [
    "FarmerID", "Location", "Address type",
    "K022-Nearest Mandi Name",
]

# Columns that need target encoding (high-cardinality categoricals)
TARGET_ENCODE_COLS = ["State", "REGION", "CITY", "DISTRICT", "VILLAGE", "Zipcode"]

# Binary / low-cardinality categoricals to encode
BINARY_ENCODE_COLS = ["SEX", "MARITAL_STATUS", "Ownership"]

# Ordinal categoricals (Good > Average > Poor)
ORDINAL_COLS = [
    "K022-Village category based on Agri parameters (Good, Average, Poor)",
    "K022-Village category based on socio-economic parameters (Good, Average, Poor)",
    "R022-Village category based on Agri parameters (Good, Average, Poor)",
    " Village category based on socio-economic parameters (Good, Average, Poor)",
]
ORDINAL_MAP = {"Poor": 0, "Average": 1, "Good": 2}

# Temperature columns to parse into min / max / range
TEMPERATURE_COLS = [
    "K022-Ambient temperature (min & max)",
    "R022-Ambient temperature (min & max)",
    "K021-Ambient temperature (min & max)",
    "R021-Ambient temperature (min & max)",
    "R020-Ambient temperature (min & max)",
]

# Categorical soil / water-body columns to one-hot encode
ONEHOT_COLS = [
    "Kharif Seasons Type of soil in 2020",
    "Rabi Seasons Type of soil in 2020",
    "Kharif Seasons Type of water bodies in hectares 2020",
    "Rabi Seasons Type of water bodies in hectares 2020",
    "Kharif Seasons  Type of soil in 2022",
    "Rabi Seasons Type of soil in 2022",
    "Kharif Seasons  Type of water bodies in hectares 2022",
    "Rabi Seasons Type of water bodies in hectares 2022",
    "Kharif Seasons Type of soil in 2021",
    "Rabi Seasons Type of soil in 2021",
    "Kharif Seasons Type of water bodies in hectares 2021",
    "Rabi Seasons Type of water bodies in hectares 2021",
]

# Columns to log-transform (highly skewed)
LOG_TRANSFORM_COLS = [
    "No_of_Active_Loan_In_Bureau",
    "Non_Agriculture_Income",
    "Avg_Disbursement_Amount_Bureau",
]

# Numerical columns used for feature engineering
LAND_COL = "Total_Land_For_Agriculture"
NON_AGRI_INCOME = "Non_Agriculture_Income"
SOCIO_SCORE = "KO22-Village score based on socio-economic parameters (0 to 100)"
MANDI_DIST = "K022-Proximity to nearest mandi (Km)"
RAILWAY_DIST = "K022-Proximity to nearest railway (Km)"
NIGHT_LIGHT = " Night light index"
ROAD_DENSITY = " Road density (Km/ SqKm)"
LAND_HOLDING_IDX = " Land Holding Index source (Total Agri Area/ no of people)"
KCC_COL = "perc_Households_do_not_have_KCC_With_The_Credit_Limit_Of_50k"

# Infrastructure columns
INFRA_COLS = [
    "perc_of_pop_living_in_hh_electricity",
    "Perc_of_house_with_6plus_room",
    "perc_Households_with_Pucca_House_That_Has_More_Than_3_Rooms",
    "mat_roof_Metal_GI_Asbestos_sheets",
    "perc_of_Wall_material_with_Burnt_brick",
    "Households_with_improved_Sanitation_Facility",
]

# Agricultural score columns (for trend features)
AGRI_SCORE_COLS = {
    "kharif_2022": "Kharif Seasons  Agricultural Score in 2022",
    "rabi_2022": "Rabi Seasons Agricultural Score in 2022",
    "kharif_2021": "Kharif Seasons Agricultural Score in 2021",
    "rabi_2021": "Rabi Seasons Agricultural Score in 2021",
    "kharif_2020": "Kharif Seasons Agricultural Score in 2020",
    "rabi_2020": "Rabi Seasons Agricultural Score in 2020",
}

# Rainfall columns (for trend & variability)
RAINFALL_COLS = [
    "K022-Seasonal Average Rainfall (mm)",
    "R022-Seasonal Average Rainfall (mm)",
    "K021-Seasonal Average Rainfall (mm)",
    "R021-Seasonal Average Rainfall (mm)",
    "R020-Seasonal Average Rainfall (mm)",
]

# ---------------------------------------------------------------------------
# LightGBM Hyperparameters
# ---------------------------------------------------------------------------
LGB_PARAMS = {
    "objective": "regression_l1",
    "metric": "mape",
    "learning_rate": 0.05,
    "num_leaves": 31,
    "feature_fraction": 0.9,
    "bagging_fraction": 0.8,
    "bagging_freq": 5,
    "min_child_samples": 30,
    "reg_alpha": 0.1,
    "reg_lambda": 0.1,
    "verbose": -1,
    "n_jobs": -1,
    "seed": SEED,
}

NUM_BOOST_ROUNDS = 2000
EARLY_STOPPING_ROUNDS = 100

# Target encoding smoothing factor
TE_SMOOTHING = 20
