"""
Training module: 5-Fold CV with LightGBM.
Prints train vs val MAPE per fold to verify generalization.
Saves fold models and diagnostic plots.
"""

import os
import sys
import numpy as np
import pandas as pd
import lightgbm as lgb
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_percentage_error

import config as cfg


def train_model(X_train, y_train):
    """
    Train LightGBM with 5-Fold CV.

    Returns:
        models: list of trained models (one per fold)
        oof_preds: out-of-fold predictions
        results: dict with per-fold and overall metrics
    """
    os.makedirs(cfg.MODEL_DIR, exist_ok=True)
    os.makedirs(cfg.REPORT_DIR, exist_ok=True)

    kf = KFold(n_splits=cfg.N_FOLDS, shuffle=True, random_state=cfg.SEED)
    models = []
    oof_preds = np.zeros(len(X_train))
    fold_results = []

    print("=" * 60)
    print(f"TRAINING: {cfg.N_FOLDS}-Fold Cross-Validation")
    print("=" * 60)

    for fold, (train_idx, val_idx) in enumerate(kf.split(X_train), 1):
        print(f"\n--- Fold {fold}/{cfg.N_FOLDS} ---")

        X_tr = X_train.iloc[train_idx]
        y_tr = y_train.iloc[train_idx]
        X_val = X_train.iloc[val_idx]
        y_val = y_train.iloc[val_idx]

        lgb_train = lgb.Dataset(X_tr, y_tr)
        lgb_val = lgb.Dataset(X_val, y_val, reference=lgb_train)

        model = lgb.train(
            cfg.LGB_PARAMS,
            lgb_train,
            num_boost_round=cfg.NUM_BOOST_ROUNDS,
            valid_sets=[lgb_train, lgb_val],
            valid_names=["train", "val"],
            callbacks=[
                lgb.early_stopping(cfg.EARLY_STOPPING_ROUNDS, verbose=False),
                lgb.log_evaluation(200),
            ],
        )

        # Predictions
        train_preds = model.predict(X_tr, num_iteration=model.best_iteration)
        val_preds = model.predict(X_val, num_iteration=model.best_iteration)
        oof_preds[val_idx] = val_preds

        # Log-scale MAPE (comparable to old baseline ~1.4%)
        train_mape_log = mean_absolute_percentage_error(y_tr, train_preds)
        val_mape_log = mean_absolute_percentage_error(y_val, val_preds)
        gap_log = val_mape_log - train_mape_log

        # Real-scale MAPE (after inverse transform — inflated by outliers)
        train_mape_real = mean_absolute_percentage_error(np.expm1(y_tr), np.expm1(train_preds))
        val_mape_real = mean_absolute_percentage_error(np.expm1(y_val), np.expm1(val_preds))

        fold_results.append({
            "fold": fold,
            "train_mape_log": train_mape_log,
            "val_mape_log": val_mape_log,
            "gap_log": gap_log,
            "train_mape_real": train_mape_real,
            "val_mape_real": val_mape_real,
            "best_iteration": model.best_iteration,
        })

        print(f"  Log-scale  → Train: {train_mape_log:.4%}  Val: {val_mape_log:.4%}  Gap: {gap_log:.4%}")
        print(f"  Real-scale → Train: {train_mape_real:.4%}  Val: {val_mape_real:.4%}")
        print(f"  Best iteration: {model.best_iteration}")

        # Save model
        model_path = os.path.join(cfg.MODEL_DIR, f"lgb_fold{fold}.pkl")
        joblib.dump(model, model_path)
        models.append(model)

    # --- Overall results ---
    results_df = pd.DataFrame(fold_results)

    # Log-scale metrics (the primary comparison metric)
    oof_mape_log = mean_absolute_percentage_error(y_train, oof_preds)
    mean_val_log = results_df["val_mape_log"].mean()
    std_val_log = results_df["val_mape_log"].std()
    mean_gap_log = results_df["gap_log"].mean()

    # Real-scale metrics
    oof_mape_real = mean_absolute_percentage_error(np.expm1(y_train), np.expm1(oof_preds))

    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"  📊 Log-scale OOF MAPE:  {oof_mape_log:.4%}  (compare to baseline ~1.4%)")
    print(f"  📊 Real-scale OOF MAPE: {oof_mape_real:.4%}  (inflated by outliers, expected)")
    print(f"  Mean Val MAPE (log):    {mean_val_log:.4%} ± {std_val_log:.4%}")
    print(f"  Mean Train-Val Gap:     {mean_gap_log:.4%}")
    print(f"  CV Stability:  {'✅ Stable' if std_val_log < 0.001 else '⚠️ Check (std=' + f'{std_val_log:.4%}' + ')'}")
    print(f"  Generalization: {'✅ OK' if abs(mean_gap_log) < 0.003 else '⚠️ Gap = ' + f'{mean_gap_log:.4%}'}")

    results = {
        "fold_results": results_df,
        "oof_mape_log": oof_mape_log,
        "oof_mape_real": oof_mape_real,
        "overall_oof_mape": oof_mape_log,  # used by pipeline summary
        "mean_val_mape": mean_val_log,
        "std_val_mape": std_val_log,
        "mean_gap": mean_gap_log,
    }

    # --- Plots ---
    _plot_feature_importance(models, X_train.columns)
    _plot_fold_results(results_df)
    _plot_residuals(y_train, oof_preds)

    return models, oof_preds, results


def _plot_feature_importance(models, feature_names, top_n=25):
    """Plot average feature importance across all folds."""
    importance = np.zeros(len(feature_names))
    for model in models:
        importance += model.feature_importance(importance_type="gain")
    importance /= len(models)

    feat_imp = pd.DataFrame({"feature": feature_names, "importance": importance})
    feat_imp = feat_imp.sort_values("importance", ascending=True).tail(top_n)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(feat_imp["feature"], feat_imp["importance"], color="#4CAF50")
    ax.set_title(f"Top {top_n} Feature Importance (Gain)", fontsize=14)
    ax.set_xlabel("Average Gain")
    plt.tight_layout()
    plt.savefig(os.path.join(cfg.REPORT_DIR, "feature_importance.png"), dpi=150)
    plt.close()
    print("  Saved: reports/feature_importance.png")


def _plot_fold_results(results_df):
    """Bar chart comparing train vs val MAPE per fold."""
    fig, ax = plt.subplots(figsize=(8, 5))
    x = results_df["fold"]
    w = 0.35
    ax.bar(x - w / 2, results_df["train_mape_log"] * 100, w, label="Train MAPE", color="#2196F3")
    ax.bar(x + w / 2, results_df["val_mape_log"] * 100, w, label="Val MAPE", color="#FF5722")
    ax.set_xlabel("Fold")
    ax.set_ylabel("MAPE (%)")
    ax.set_title("Train vs Validation MAPE per Fold")
    ax.legend()
    ax.set_xticks(x)
    plt.tight_layout()
    plt.savefig(os.path.join(cfg.REPORT_DIR, "fold_results.png"), dpi=150)
    plt.close()
    print("  Saved: reports/fold_results.png")


def _plot_residuals(y_true, y_pred_log):
    """Scatter plot of predicted vs actual (in original scale)."""
    y_actual = np.expm1(y_true)
    y_pred = np.expm1(y_pred_log)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Predicted vs Actual
    axes[0].scatter(y_actual, y_pred, alpha=0.1, s=5, color="#673AB7")
    max_val = max(y_actual.max(), y_pred.max())
    axes[0].plot([0, max_val], [0, max_val], "r--", alpha=0.8)
    axes[0].set_xlabel("Actual Income")
    axes[0].set_ylabel("Predicted Income")
    axes[0].set_title("Predicted vs Actual")

    # Residual distribution
    residuals = (y_pred - y_actual) / y_actual * 100  # percentage error
    axes[1].hist(residuals.clip(-50, 50), bins=100, color="#009688", edgecolor="white")
    axes[1].set_xlabel("Percentage Error (%)")
    axes[1].set_ylabel("Count")
    axes[1].set_title("Residual Distribution")
    axes[1].axvline(0, color="red", linestyle="--")

    plt.tight_layout()
    plt.savefig(os.path.join(cfg.REPORT_DIR, "residual_analysis.png"), dpi=150)
    plt.close()
    print("  Saved: reports/residual_analysis.png")


if __name__ == "__main__":
    # If run directly, prepare data then train
    sys.path.insert(0, os.path.dirname(__file__))
    from data_prep import prepare_datasets

    X_train, y_train, X_test, farmer_ids = prepare_datasets()
    models, oof_preds, results = train_model(X_train, y_train)
