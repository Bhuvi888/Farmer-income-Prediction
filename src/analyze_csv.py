

import pandas as pd

# Define the path to your CSV file
file_path = r'C:\Users\ACER\Downloads\ltf hackathon\traindata.csv'

try:
    # Read the CSV file into a pandas DataFrame
    print("Loading data from CSV...")
    # Use a low_memory=False to avoid potential mixed-type inference issues with large files
    df = pd.read_csv(file_path, low_memory=False)
    print("Data loaded successfully.")

    # Display a concise summary of the DataFrame
    print("\n" + "="*30)
    print("DataFrame Info (Data Types & Null Counts)")
    print("="*30)
    df.info(verbose=True, show_counts=True)

    # Display descriptive statistics for numerical columns
    print("\n" + "="*30)
    print("Descriptive Statistics (Numerical Columns)")
    print("="*30)
    print(df.describe())

except FileNotFoundError:
    print(f"Error: The file was not found at the specified path.")
except Exception as e:
    print(f"An error occurred: {e}")

