# Farmer Income Prediction Project

This project aims to predict farmer income to assess creditworthiness, using LightGBM.

## Project Structure

- `src/`: Contains all Python scripts for data cleaning, feature engineering, model training, and prediction.
- `data/raw/`: Stores the raw input datasets.
- `data/docs/`: Contains project documentation.
- `models/`: Stores the trained machine learning models.
- `predictions/`: Stores the generated income predictions.
- `reports/`: Contains EDA plots and other reports.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd ltf-hackathon
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the full pipeline and generate predictions:

1.  **Data Cleaning and Preprocessing:**
    ```bash
    python src/data_cleaning.py
    python src/preprocess_test_data.py
    ```
2.  **Feature Engineering (Geographical and Seasonal):**
    ```bash
    python src/feature_engineering_geo.py
    python src/feature_engineering_seasonal.py
    ```
3.  **Model Training and Tuning:**
    ```bash
    python src/train_lightgbm.py
    python src/tune_lightgbm.py
    ```
4.  **Generate Predictions:**
    ```bash
    python src/predict_test_data.py
    ```

## Results

- Final predictions are saved in `predictions/Predicted_Farmer_Income.csv`.
- EDA plots are available in `reports/`.
- The best-performing model is saved as `models/best_lightgbm_model.pkl`.
