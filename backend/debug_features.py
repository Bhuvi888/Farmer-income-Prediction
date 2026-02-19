"""Check which top features are getting inflated defaults."""
import json, joblib

model = joblib.load("models/lgb_fold1.pkl")
defaults = json.load(open("models/feature_defaults.json"))

# Top 25 features by importance
imp = dict(zip(model.feature_name(), model.feature_importance("gain")))
top = sorted(imp.items(), key=lambda x: -x[1])[:30]

print(f"{'Feature':<60} {'Importance':>10} {'Default':>12}")
print("-" * 85)
for name, importance in top:
    val = defaults.get(name, 0)
    print(f"{name:<60} {importance:>10.0f} {val:>12.2f}")
