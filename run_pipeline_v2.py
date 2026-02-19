"""
Pipeline orchestrator: runs data prep → training → prediction.
"""

import os
import sys
import time

# Ensure src/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from data_prep import prepare_datasets
from train import train_model
from predict import predict


def main():
    start = time.time()

    print("\n" + "=" * 60)
    print("  FARMER INCOME PREDICTION PIPELINE v2")
    print("=" * 60)

    # Step 1: Prepare data
    print("\n📦 Preparing datasets...")
    X_train, y_train, X_test, farmer_ids = prepare_datasets()

    # Step 2: Train model
    print("\n🚀 Training model...")
    models, oof_preds, results = train_model(X_train, y_train)

    # Step 3: Generate predictions
    print("\n📊 Generating predictions...")
    submission = predict(X_test, farmer_ids)

    # Summary
    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
    print(f"  Time: {elapsed:.1f}s")
    print(f"  OOF MAPE: {results['overall_oof_mape']:.4%}")
    print(f"  CV Stability: ±{results['std_val_mape']:.4%}")
    print(f"  Predictions: {len(submission)} farmers")
    print(f"  Output: predictions/Predicted_Farmer_Income_v2.csv")
    print(f"  Reports: reports/")


if __name__ == "__main__":
    main()
