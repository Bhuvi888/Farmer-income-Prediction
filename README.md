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

## License

By participating in the LTF Pearl Anniversary Challenge and submitting a model, participants agree to transfer all intellectual property rights associated with the submitted models to L&T Finance Limited (LTF). LTF retains exclusive rights to use, modify, and integrate the model into their creditworthiness evaluation tools and other related projects. The use of LTF data, including the submitted model and its code, for any commercial and non-commercial publication (blog, tutorials, research publications) requires prior approval and permission from LTF.

## 5. How to Run

## Usage

To run the full pipeline and generate predictions automatically, execute:

```bash
python run_pipeline.py
```

Alternatively, you can run each step manually:

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

- **Baseline LightGBM Model (before feature engineering):** MAPE of 1.68%
- **After Initial Feature Engineering (excluding geographical and seasonal):** MAPE improved to 1.59%
- **After Initial Hyperparameter Tuning (excluding geographical and seasonal):** MAPE further improved to 1.546%
- **After Geographical Feature Engineering (retraining):** MAPE improved to approximately 1.47%
- **After Geographical Feature Engineering (hyperparameter tuning):** MAPE further improved to approximately 1.439%
- **After Seasonal Interaction Feature Engineering (retraining):** MAPE was approximately 1.472%
- **After Seasonal Interaction Feature Engineering (hyperparameter tuning):** Final MAPE of approximately 1.436% on the validation set.

- Final predictions are saved in `predictions/Predicted_Farmer_Income.csv`.
- EDA plots are available in `reports/`.
- The best-performing model is saved as `models/best_lightgbm_model.pkl`.
