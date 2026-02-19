"""
Prediction module: load fold models, ensemble predictions, save results.
"""

import os
import sys
import numpy as np
import pandas as pd
import joblib

import config as cfg


def predict(X_test, farmer_ids, model_dir=None):
    """
    Load all fold models and average their predictions.

    Args:
        X_test: prepared test features
        farmer_ids: FarmerID series for the submission file
        model_dir: path to saved models (default: cfg.MODEL_DIR)

    Returns:
        submission DataFrame with FarmerID and Predicted_Income
    """
    if model_dir is None:
        model_dir = cfg.MODEL_DIR

    os.makedirs(cfg.PRED_DIR, exist_ok=True)

    # Load all fold models
    model_files = sorted([f for f in os.listdir(model_dir) if f.startswith("lgb_fold")])
    if not model_files:
        raise FileNotFoundError(f"No fold models found in {model_dir}")

    print(f"Loading {len(model_files)} fold models...")
    predictions = np.zeros(len(X_test))

    for model_file in model_files:
        model = joblib.load(os.path.join(model_dir, model_file))
        preds = model.predict(X_test, num_iteration=model.best_iteration)
        predictions += preds
        print(f"  {model_file}: done")

    # Average across folds
    predictions /= len(model_files)

    # Inverse log transform to get actual income values
    predictions = np.expm1(predictions)

    # Clip negatives (shouldn't happen, but just in case)
    predictions = np.clip(predictions, 0, None)

    # Create submission
    submission = pd.DataFrame({
        "FarmerID": farmer_ids,
        "Predicted_Income": predictions,
    })

    output_path = os.path.join(cfg.PRED_DIR, "Predicted_Farmer_Income_v2.csv")
    submission.to_csv(output_path, index=False)

    print(f"\nPredictions saved to {output_path}")
    print(f"  Shape: {submission.shape}")
    print(f"  Income range: {predictions.min():,.0f} — {predictions.max():,.0f}")
    print(f"  Mean predicted income: {predictions.mean():,.0f}")

    return submission


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(__file__))
    from data_prep import prepare_datasets

    X_train, y_train, X_test, farmer_ids = prepare_datasets()
    submission = predict(X_test, farmer_ids)
