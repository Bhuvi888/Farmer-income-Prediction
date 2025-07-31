import pandas as pd

# Load the cleaned data
df = pd.read_csv('TrainData_cleaned.csv', low_memory=False)

print("--- Dataset Overview ---")

# Display shape
print(f"\nShape of the dataset: {df.shape}")

# Display header
print("\nFirst 5 rows:")
print(df.head())

# Display info
print("\nData types and null values:")
df.info()

# Display descriptive statistics
print("\nDescriptive statistics for numerical columns:")
print(df.describe())
