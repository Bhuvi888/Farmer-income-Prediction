import subprocess
import os

def run_command(command, description):
    print(f"\n--- {description} ---")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"[WARNING] Stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e.cmd}")
        print(f"[ERROR] Stdout: {e.stdout}")
        print(f"[ERROR] Stderr: {e.stderr}")
        exit(1)
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    print("Starting the full Farmer Income Prediction pipeline...")

    # Change to the src directory to run scripts correctly
    original_dir = os.getcwd()
    script_dir = os.path.dirname(__file__)
    os.chdir(os.path.join(script_dir, 'src'))

    # 1. Data Cleaning and Preprocessing
    run_command("python data_cleaning.py", "Running Data Cleaning for Training Data")
    run_command("python preprocess_test_data.py", "Running Preprocessing for Test Data")

    # 2. Feature Engineering
    run_command("python feature_engineering_geo.py", "Running Geographical Feature Engineering")
    run_command("python feature_engineering_seasonal.py", "Running Seasonal Interaction Feature Engineering")

    # 3. Model Training and Tuning
    run_command("python train_lightgbm.py", "Running LightGBM Model Training")
    run_command("python tune_lightgbm.py", "Running LightGBM Hyperparameter Tuning")

    # 4. Prediction Generation
    run_command("python predict_test_data.py", "Generating Predictions on Test Data")

    # Change back to the original directory
    os.chdir(original_dir)

    print("\nFull pipeline execution completed successfully!")
