

import pandas as pd

file_path = r'C:\Users\ACER\Downloads\ltf hackathon\traindata.csv'

try:
    df = pd.read_csv(file_path, low_memory=False)
    
    # Analyze Target_Variable/Total Income
    print("Analyzing Target_Variable/Total Income...")
    null_count = df['Target_Variable/Total Income'].isnull().sum()
    print(f"Null values: {null_count}")
    print(f"Percentage missing: {null_count / len(df) * 100:.2f}%")
    print("\nDescriptive Statistics (Non-null values):")
    print(df['Target_Variable/Total Income'].dropna().describe())

except FileNotFoundError:
    print(f"Error: The file was not found at the specified path.")
except Exception as e:
    print(f"An error occurred: {e}")

