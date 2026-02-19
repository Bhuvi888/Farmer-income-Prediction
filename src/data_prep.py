"""
Data preparation module: loading, cleaning, feature engineering, encoding.

Each function does one clear job. Call prepare_datasets() to get
ready-to-train X_train, y_train, X_test, and the FarmerIDs for test.
"""

import pandas as pd
import numpy as np
import re
from sklearn.model_selection import KFold

import config as cfg


# ===================================================================
# 1. LOADING
# ===================================================================

def load_data():
    """Load raw train & test CSVs and clean column names."""
    train = pd.read_csv(cfg.TRAIN_RAW, low_memory=False)
    test = pd.read_csv(cfg.TEST_RAW, low_memory=False)

    # Strip whitespace from column names
    train.columns = train.columns.str.strip()
    test.columns = test.columns.str.strip()

    print(f"Loaded train: {train.shape}, test: {test.shape}")
    return train, test


# ===================================================================
# 2. CLEANING
# ===================================================================

def handle_missing(df):
    """Fill nulls: median for numeric, mode for categorical."""
    for col in df.select_dtypes(include="number").columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    for col in df.select_dtypes(include="object").columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")

    return df


def handle_outliers(df, target_col):
    """Cap target variable at 99th percentile to reduce extreme outliers."""
    if target_col in df.columns:
        cap = df[target_col].quantile(0.99)
        df[target_col] = df[target_col].clip(upper=cap)
        print(f"Capped {target_col} at {cap:,.0f}")
    return df


def parse_temperature(df, temp_cols):
    """Parse 'min & max' temperature strings into separate numeric columns."""
    for col in temp_cols:
        if col not in df.columns:
            continue
        df[col] = df[col].astype(str)
        splits = df[col].apply(lambda x: re.split(r'\s*&\s*|\s*/\s*', x))
        df[col + "_min"] = pd.to_numeric(splits.apply(lambda x: x[0] if len(x) > 0 else None), errors="coerce")
        df[col + "_max"] = pd.to_numeric(splits.apply(lambda x: x[1] if len(x) > 1 else None), errors="coerce")
        df[col + "_range"] = df[col + "_max"] - df[col + "_min"]
        df.drop(columns=[col], inplace=True)
    return df


def log_transform(df, cols, target_col=None):
    """Apply log1p to skewed numeric columns. Optionally also to target."""
    for col in cols:
        if col in df.columns:
            df[col] = np.log1p(df[col].clip(lower=0))
    if target_col and target_col in df.columns:
        df[target_col] = np.log1p(df[target_col].clip(lower=0))
    return df


# ===================================================================
# 3. ENCODING
# ===================================================================

def encode_binary(df, cols):
    """Label-encode binary / low-cardinality categoricals (0, 1, 2, ...)."""
    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype("category").cat.codes
    return df


def encode_ordinal(df, cols, mapping):
    """Map ordinal categories to integers using the given mapping."""
    for col in cols:
        if col in df.columns:
            df[col] = df[col].map(mapping).fillna(-1).astype(int)
    return df


def encode_onehot(df, cols):
    """One-hot encode categorical columns (soil types, water bodies, etc.)."""
    for col in cols:
        if col in df.columns:
            df = pd.get_dummies(df, columns=[col], dummy_na=False)
    return df


def target_encode_kfold(train, test, cols, target_col, n_folds=5, smoothing=20, seed=42):
    """
    K-Fold target encoding to prevent leakage.

    For train: each row's encoding uses only data from OTHER folds.
    For test:  uses the full training set mean per category.
    Smoothing blends category mean with global mean for rare categories.
    """
    global_mean = train[target_col].mean()
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=seed)

    for col in cols:
        if col not in train.columns:
            continue

        enc_col = f"{col}_te"

        # --- Train: out-of-fold encoding ---
        train[enc_col] = np.nan
        for fold_train_idx, fold_val_idx in kf.split(train):
            fold_train = train.iloc[fold_train_idx]
            stats = fold_train.groupby(col)[target_col].agg(["mean", "count"])
            smoothed = (stats["count"] * stats["mean"] + smoothing * global_mean) / (stats["count"] + smoothing)
            train.loc[train.index[fold_val_idx], enc_col] = (
                train.iloc[fold_val_idx][col].map(smoothed)
            )
        train[enc_col] = train[enc_col].fillna(global_mean)

        # --- Test: full training set encoding ---
        stats = train.groupby(col)[target_col].agg(["mean", "count"])
        smoothed = (stats["count"] * stats["mean"] + smoothing * global_mean) / (stats["count"] + smoothing)
        test[enc_col] = test[col].map(smoothed).fillna(global_mean)

    return train, test


# ===================================================================
# 4. FEATURE ENGINEERING
# ===================================================================

def create_village_population(train, test):
    """Village population proxy = count of farmers per village."""
    village_counts = train["VILLAGE"].value_counts().to_dict()
    train["Village_Population"] = train["VILLAGE"].map(village_counts)
    test["Village_Population"] = test["VILLAGE"].map(village_counts).fillna(1)
    return train, test


def engineer_features(df):
    """
    Create all derived features. Works on both train and test.
    All input columns should already be cleaned and numeric at this point.
    """
    # --- Interaction features ---
    if cfg.LAND_COL in df.columns and cfg.SOCIO_SCORE in df.columns:
        df["Land_x_SocioScore"] = df[cfg.LAND_COL] * df[cfg.SOCIO_SCORE]

    if cfg.NIGHT_LIGHT in df.columns and cfg.ROAD_DENSITY in df.columns:
        df["NightLight_x_RoadDensity"] = df[cfg.NIGHT_LIGHT] * df[cfg.ROAD_DENSITY]

    if cfg.NON_AGRI_INCOME in df.columns and cfg.LAND_COL in df.columns:
        df["Income_x_Land"] = df[cfg.NON_AGRI_INCOME] * df[cfg.LAND_COL]

    if cfg.SOCIO_SCORE in df.columns and cfg.MANDI_DIST in df.columns:
        df["SocioScore_x_MandiDist"] = df[cfg.SOCIO_SCORE] * df[cfg.MANDI_DIST]

    # --- Ratio features ---
    if "Avg_Disbursement_Amount_Bureau" in df.columns and cfg.NON_AGRI_INCOME in df.columns:
        df["Loan_to_Income_Ratio"] = df["Avg_Disbursement_Amount_Bureau"] / (df[cfg.NON_AGRI_INCOME] + 1)

    if cfg.LAND_COL in df.columns and "Village_Population" in df.columns:
        df["Land_per_Person"] = df[cfg.LAND_COL] / (df["Village_Population"] + 1)

    if cfg.MANDI_DIST in df.columns and cfg.RAILWAY_DIST in df.columns:
        df["Market_Access_Score"] = 1 / (1 + df[cfg.MANDI_DIST]) * 1 / (1 + df[cfg.RAILWAY_DIST])

    # --- Polynomial features ---
    if cfg.LAND_COL in df.columns:
        df["Land_sq"] = df[cfg.LAND_COL] ** 2

    if cfg.NON_AGRI_INCOME in df.columns:
        df["NonAgriIncome_sq"] = df[cfg.NON_AGRI_INCOME] ** 2

    # --- Infrastructure composite score ---
    infra_present = [c for c in cfg.INFRA_COLS if c in df.columns]
    if infra_present:
        df["Infrastructure_Score"] = df[infra_present].mean(axis=1)

    # --- Agricultural performance trend (2022 vs 2020) ---
    scores = cfg.AGRI_SCORE_COLS
    if scores["kharif_2022"] in df.columns and scores["kharif_2020"] in df.columns:
        df["Agri_Trend_Kharif"] = df[scores["kharif_2022"]] - df[scores["kharif_2020"]]
    if scores["rabi_2022"] in df.columns and scores["rabi_2020"] in df.columns:
        df["Agri_Trend_Rabi"] = df[scores["rabi_2022"]] - df[scores["rabi_2020"]]

    # Average agricultural score across all seasons/years
    score_cols = [c for c in scores.values() if c in df.columns]
    if score_cols:
        df["Avg_Agri_Score"] = df[score_cols].mean(axis=1)

    # --- Rainfall variability ---
    rain_present = [c for c in cfg.RAINFALL_COLS if c in df.columns]
    if len(rain_present) >= 2:
        df["Rainfall_Variability"] = df[rain_present].std(axis=1)
        df["Rainfall_Mean"] = df[rain_present].mean(axis=1)
        # Trend: most recent - oldest
        df["Rainfall_Trend"] = df[rain_present[0]] - df[rain_present[-1]]

    # --- KCC feature ---
    if cfg.KCC_COL in df.columns:
        df["KCC_Access"] = 100 - df[cfg.KCC_COL]  # invert: higher = more access

    return df


def add_state_aggregations(train, test, cols_to_agg, group_col="State"):
    """
    State-level mean aggregations. Uses K-Fold style to avoid leakage on train.
    """
    global_means = {}
    kf = KFold(n_splits=cfg.N_FOLDS, shuffle=True, random_state=cfg.SEED)

    for col in cols_to_agg:
        if col not in train.columns:
            continue

        agg_name = f"{group_col}_Avg_{col}"
        global_means[col] = train[col].mean()

        # Out-of-fold for train
        train[agg_name] = np.nan
        for fold_train_idx, fold_val_idx in kf.split(train):
            fold_train = train.iloc[fold_train_idx]
            state_means = fold_train.groupby(group_col)[col].mean().to_dict()
            train.loc[train.index[fold_val_idx], agg_name] = (
                train.iloc[fold_val_idx][group_col].map(state_means)
            )
        train[agg_name] = train[agg_name].fillna(global_means[col])

        # Full map for test
        state_means = train.groupby(group_col)[col].mean().to_dict()
        test[agg_name] = test[group_col].map(state_means).fillna(global_means[col])

    return train, test


# ===================================================================
# 5. CLEAN COLUMN NAMES (for LightGBM compatibility)
# ===================================================================

def clean_column_names(df):
    """Replace special characters in column names with underscores."""
    df.columns = [re.sub(r'[^A-Za-z0-9_]+', '_', col).strip('_') for col in df.columns]
    return df


# ===================================================================
# 6. MAIN: PREPARE DATASETS
# ===================================================================

def prepare_datasets():
    """
    Full pipeline: load → clean → encode → engineer → return ready data.

    Returns:
        X_train (DataFrame), y_train (Series), X_test (DataFrame), farmer_ids (Series)
    """
    print("=" * 60)
    print("STEP 1: Loading data")
    print("=" * 60)
    train, test = load_data()
    farmer_ids = test["FarmerID"].copy()

    print("\nSTEP 2: Cleaning")
    print("-" * 40)
    # Parse temperature before anything else (creates new columns)
    train = parse_temperature(train, cfg.TEMPERATURE_COLS)
    test = parse_temperature(test, cfg.TEMPERATURE_COLS)

    # Handle outliers in target
    train = handle_outliers(train, cfg.TARGET_COL_RAW)

    # Handle missing values
    train = handle_missing(train)
    test = handle_missing(test)

    print("\nSTEP 3: Encoding categoricals")
    print("-" * 40)
    # Binary & ordinal encoding
    train = encode_binary(train, cfg.BINARY_ENCODE_COLS)
    test = encode_binary(test, cfg.BINARY_ENCODE_COLS)
    train = encode_ordinal(train, cfg.ORDINAL_COLS, cfg.ORDINAL_MAP)
    test = encode_ordinal(test, cfg.ORDINAL_COLS, cfg.ORDINAL_MAP)

    # One-hot encode soil/water types
    train = encode_onehot(train, cfg.ONEHOT_COLS)
    test = encode_onehot(test, cfg.ONEHOT_COLS)

    # Village population (before target encoding)
    train, test = create_village_population(train, test)

    # Log transform skewed columns + target
    train = log_transform(train, cfg.LOG_TRANSFORM_COLS, target_col=cfg.TARGET_COL_RAW)
    test = log_transform(test, cfg.LOG_TRANSFORM_COLS)

    # K-Fold target encoding (leakage-free)
    print("  Applying K-Fold target encoding...")
    train, test = target_encode_kfold(
        train, test, cfg.TARGET_ENCODE_COLS,
        target_col=cfg.TARGET_COL_RAW,
        n_folds=cfg.N_FOLDS,
        smoothing=cfg.TE_SMOOTHING,
        seed=cfg.SEED,
    )

    print("\nSTEP 4: Feature engineering")
    print("-" * 40)
    train = engineer_features(train)
    test = engineer_features(test)

    # State-level aggregations (leakage-free)
    agg_cols = [c for c in [cfg.LAND_COL, cfg.NON_AGRI_INCOME, cfg.SOCIO_SCORE] if c in train.columns]
    train, test = add_state_aggregations(train, test, agg_cols)

    print("\nSTEP 5: Final cleanup")
    print("-" * 40)
    # Extract target
    y_train = train[cfg.TARGET_COL_RAW].copy()

    # Drop columns not needed for training
    cols_to_drop = cfg.DROP_COLS + cfg.TARGET_ENCODE_COLS + [cfg.TARGET_COL_RAW]
    train.drop(columns=[c for c in cols_to_drop if c in train.columns], inplace=True)
    test.drop(columns=[c for c in cols_to_drop if c in test.columns], inplace=True)

    # Clean column names for LightGBM
    train = clean_column_names(train)
    test = clean_column_names(test)

    # Align columns: ensure train and test have the same features
    common_cols = sorted(set(train.columns) & set(test.columns))
    # Only keep numeric columns
    train = train[common_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
    test = test[common_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

    print(f"\n  Final train shape: {train.shape}")
    print(f"  Final test shape:  {test.shape}")
    print(f"  Number of features: {len(common_cols)}")

    return train, y_train, test, farmer_ids


# Quick test when run directly
if __name__ == "__main__":
    X_train, y_train, X_test, ids = prepare_datasets()
    print(f"\nDone! Train: {X_train.shape}, Test: {X_test.shape}")
    print(f"Target stats: mean={y_train.mean():.4f}, std={y_train.std():.4f}")
