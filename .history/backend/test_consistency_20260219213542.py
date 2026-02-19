import requests
import json

URL = "http://localhost:5000/api/predict"
# Low Income Profile (matches frontend demo)
payload = {
    "land_size": 1.5,
    "irrigated_percentage": 10,
    "soil_type": "Sandy",
    "crop_type": "Pulses",
    "season": "Rabi",
    "yield_per_acre": 6,
    "rainfall": 400,
    "temperature": 25,
    "market_price": 4200,
    "market_distance": 35
}

response = requests.post(URL, json=payload)
data = response.json()

print(f"Predicted Income: {data['predicted_income']}")
print(f"Fold Predictions: {data['fold_predictions']}")
print(f"Average of Folds: {sum(data['fold_predictions']) / len(data['fold_predictions'])}")
