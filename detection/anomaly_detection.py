import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Load the column names used during training
columns_used = joblib.load('model/columns_used.pkl')

# Load new data
new_df = pd.read_csv("data/live_traffic.csv")

# Preprocessing: Select numerical columns and handle missing values
new_df_numeric = new_df.select_dtypes(include=['float64', 'int64']).fillna(0)

# Ensure consistent feature set with training data
common_columns = [col for col in columns_used if col in new_df_numeric.columns]
new_df_numeric = new_df_numeric[common_columns]

# Standardize using the same scaler (if saved, load scaler object)
scaler = StandardScaler()
new_df_scaled = scaler.fit_transform(new_df_numeric)

# Load the trained Isolation Forest model
isolation_forest = joblib.load('C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/isolation_forest_model.pkl')

# Predict anomalies
new_df['anomaly'] = isolation_forest.predict(new_df_scaled)

# Display anomalies as a DataFrame
anomalies = new_df[new_df['anomaly'] == -1]
print("Anomalies Detected in New Data:")
print(anomalies)


