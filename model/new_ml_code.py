import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Load your data (assuming it's in a DataFrame called 'df')
df = pd.read_csv("model/dataset.csv")
# Preprocessing: Fill NaN values and select numerical columns
df_numeric = df.select_dtypes(include=['float64', 'int64']).fillna(0)

# Standardizing data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_numeric)
print(df.columns)
# Fit Isolation Forest model
isolation_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
df['anomaly'] = isolation_forest.fit_predict(df_scaled)

# Add a column indicating anomalies (1 for normal, -1 for anomalies)
anomalies = df[df['anomaly'] == -1]

# Display the anomalies
print("Anomalies Detected:")
print(anomalies)

import joblib
joblib.dump(isolation_forest, 'C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/isolation_forest_model.pkl')
joblib.dump(df_numeric.columns, 'model/columns_used.pkl')


# Optionally, save results to a new CSV
# df.to_csv('anomalies_detected.csv', index=False)
