import logging
import os

# Create logs directory if it doesn't exist
if not os.path.exists("../logs"):
    os.makedirs("../logs")

logging.basicConfig(filename="../logs/anomaly_detection.log", level=logging.INFO)


# logging/anomaly_logging.py
def log_anomaly(message):
    #print("Log anomaly code")
    print(f"Anomaly Detected: {message}")
    # You can add code here to write the log to a file or send alerts

def get_logs():
    with open("../logs/anomaly_detection.log", "r") as file:
        logs = file.read()
    return logs
