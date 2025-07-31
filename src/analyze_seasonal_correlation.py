import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import os

def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))

# Define the seasonal columns to analyze
seasonal_cols = [
    'Kharif Seasons Type of soil in 2020',
    'Rabi Seasons Type of soil in 2020',
    'Kharif Seasons Type of water bodies in hectares 2020',
    'Rabi Seasons Type of water bodies in hectares 2020'
]

# Load only the necessary columns from the original TrainData.csv
try:
    script_dir = os.path.dirname(__file__)
    df_seasonal = pd.read_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'raw', 'LTF_Challenge_TrainData.csv')), usecols=seasonal_cols, low_memory=False)
    print("Seasonal data loaded successfully.")
except FileNotFoundError:
    print("Error: TrainData.csv not found.")
    exit()
except ValueError as e:
    print(f"Error loading specific columns: {e}. Ensure column names are exact and exist.")
    exit()

# Drop rows with any missing values in the selected columns for correlation analysis
df_seasonal.dropna(inplace=True)

# Calculate Cramer's V for all pairs of seasonal columns
num_cols = len(seasonal_cols)
cramers_v_matrix = pd.DataFrame(np.ones((num_cols, num_cols)), columns=seasonal_cols, index=seasonal_cols)

for i in range(num_cols):
    for j in range(i + 1, num_cols):
        col1 = seasonal_cols[i]
        col2 = seasonal_cols[j]
        v_score = cramers_v(df_seasonal[col1], df_seasonal[col2])
        cramers_v_matrix.loc[col1, col2] = v_score
        cramers_v_matrix.loc[col2, col1] = v_score

print("\nCramer's V Correlation Matrix for Seasonal Features:")
print(cramers_v_matrix)
