import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import os

script_dir = os.path.dirname(__file__)

# Load the cleaned data
df = pd.read_csv(os.path.abspath(os.path.join(script_dir, '..', 'data', 'TrainData_cleaned.csv')), low_memory=False)

# Clean column names
df.columns = [re.sub(r'[^A-Za-z0-9_]+', '_', col) for col in df.columns]

# 1. Distribution of Target Variable
plt.figure(figsize=(10, 6))
sns.histplot(df['Target_Variable_Total_Income'], kde=True)
plt.title('Distribution of Farmer Income (Log Transformed)')
plt.xlabel('Log of Total Income')
plt.ylabel('Frequency')
plt.savefig('income_distribution.png')
plt.close()

print("Generated income distribution plot.")

# 2. Correlation Analysis
plt.figure(figsize=(12, 10))
# Select a subset of numerical features for the correlation matrix
corr_features = [
    'No_of_Active_Loan_In_Bureau',
    'Avg_Disbursement_Amount_Bureau',
    'Non_Agriculture_Income',
    'Total_Land_For_Agriculture',
    'Village_Population',
    'K022_Proximity_to_nearest_mandi_Km_',
    'K022_Proximity_to_nearest_railway_Km_',
    'KO22_Village_score_based_on_socio_economic_parameters_0_to_100_',
    'Night_light_index',
    'Road_density_Km_SqKm_',
    'Target_Variable_Total_Income'
]
correlation_matrix = df[corr_features].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Key Features')
plt.savefig(os.path.abspath(os.path.join(script_dir, '..', 'reports', 'correlation_matrix.png')))
plt.close()

print("Generated correlation matrix heatmap.")

# 3. Geographical Analysis
plt.figure(figsize=(12, 6))
sns.boxplot(x='State', y='Target_Variable_Total_Income', data=df)
plt.title('Farmer Income Distribution by State')
plt.xlabel('State')
plt.ylabel('Log of Total Income')
plt.xticks(rotation=45)
plt.savefig(os.path.abspath(os.path.join(script_dir, '..', 'reports', 'income_by_state.png')))
plt.close()

print("Generated income by state boxplot.")
