import sys
import os
import pandas as pd
import joblib
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

sys.path.append(r'C:\Users\lenovo\OneDrive\Desktop\Project 1\network-anomaly-new')
from alerts.alert_system import send_alert
from log_module.anomaly_logging import log_anomaly

# Set up paths and load model
sys.path.append(r'C:\Users\lenovo\OneDrive\Desktop\Project 1\network-anomaly-new')
print("Current Working Directory:", os.getcwd())

# Load trained Isolation Forest model and column names
model = joblib.load('C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/isolation_forest_model.pkl')
trained_columns = joblib.load('C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/trained_columns.pkl')
label_encoders = joblib.load('C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/label_encoders.pkl')
imputer = joblib.load('C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/imputer.pkl')

def preprocess_data(df):
    # Replace 'unknown' string with NaN (if applicable)
    df = df.replace('unknown', np.nan)
    
    # Ensure all columns are string-type for label encoding compatibility
    df = df.astype(str)

    # Apply label encoding to specified columns if applicable
    for col in ['ip.src', 'ip.dst', 'http.request.uri']:
        if col in df.columns and col in label_encoders:
            # Transform using the existing encoder; handle unseen values by assigning -1
            df[col] = df[col].map(lambda s: label_encoders[col].transform([s])[0] if s in label_encoders[col].classes_ else -1)
        elif col in df.columns:
            # This block is optional if you strictly want to use the existing encoders
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le  # Save if new encoder is acceptable

    # Convert to numeric and handle missing values
    df = df.apply(pd.to_numeric, errors='coerce')
    transformed_data = imputer.transform(df)

    # Ensure the DataFrame has the same columns as the training set
    df = pd.DataFrame(transformed_data, columns=trained_columns)

    return df

def detect_anomalies():
    live_data = pd.read_csv(r"C:\Users\lenovo\OneDrive\Desktop\Project 1\network-anomaly-new\data\live_traffic.csv")
    live_data = preprocess_data(live_data)

    # Convert to numpy array before passing to the model
    live_data_array = live_data.to_numpy()

    # Predict using the Isolation Forest model
    y_pred = model.predict(live_data_array)

    # Isolation Forest predicts -1 for anomalies and 1 for normal points
    anomalies = live_data[y_pred == -1]

    if not anomalies.empty:
        send_alert(anomalies)
        log_anomaly(anomalies)
    return pd.DataFrame(anomalies)

if __name__ == "__main__":
    detect_anomalies() 
