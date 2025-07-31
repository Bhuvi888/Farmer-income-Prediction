import pandas as pd
import os

# Get the path of the current script (src/)
script_dir = os.path.dirname(__file__)

# Build the absolute path to the CSV file
csv_path = os.path.abspath(os.path.join(script_dir, '..', 'data', 'raw', 'TrainData.csv'))

print("Full path to CSV:", csv_path)

# Optional test to prove it's accessible
with open(csv_path, 'r') as f:
    print("File opened successfully!")

# NOW load it using pandas
df = pd.read_csv(csv_path, low_memory=False)
print("CSV loaded into DataFrame. Shape:", df.shape)
