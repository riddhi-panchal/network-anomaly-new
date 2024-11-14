import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, classification_report
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

# Load the dataset
df_large = pd.read_csv(r"C:\Users\lenovo\OneDrive\Desktop\Project 1\network-anomaly-new\model\Realistic_Large-Scale_Network_Traffic_Dataset.csv")

# Split features and target
X = df_large.drop(columns=['label'])
y = df_large['label']

# Initialize label encoders dictionary
label_encoders = {}

# Label encode high-cardinality columns
for col in ['ip.src', 'ip.dst', 'http.request.uri']:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le  # Save the encoder for later use

# Save the label encoders for prediction
joblib.dump(label_encoders, 'C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/label_encoders.pkl')

# Train-test split (using 80-20 split for evaluation)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Handle missing values by imputing with the most frequent value
imputer = SimpleImputer(strategy='most_frequent')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# Save the imputer for future use
joblib.dump(imputer, 'C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/imputer.pkl')

# Save trained column names for consistency
trained_columns = X.columns
joblib.dump(trained_columns, 'C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/trained_columns.pkl')

# Fit the Isolation Forest model
clf = IsolationForest(n_estimators=100, max_samples='auto', contamination=0.05, random_state=42)
clf.fit(X_train)

# Save the trained model
joblib.dump(clf, 'C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/model/isolation_forest_model.pkl')

# Predict using the Isolation Forest model
# Note: -1 indicates an anomaly in IsolationForest predictions, and 1 indicates normal
y_pred = clf.predict(X_test)

# Convert predictions to match your labels (0 for normal, 1 for anomalies)
y_pred = np.where(y_pred == -1, 1, 0)

# Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy}")
print("Classification Report:")
print(classification_report(y_test, y_pred))
