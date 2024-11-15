import streamlit as st
import subprocess
import os
import time
import pandas as pd

from prometheus_client import start_http_server, Counter, Gauge, CollectorRegistry

# Create a custom registry
registry = CollectorRegistry()

# Define Prometheus metrics using the custom registry
packets_captured = Counter('packets_captured_total', 'Total number of packets captured', registry=registry)
anomalies_detected = Counter('anomalies_detected_total', 'Total number of anomalies detected', registry=registry)
capture_status = Gauge('capture_status', 'Indicates if packet capture is active (1 for active, 0 for inactive)', registry=registry)

# Start Prometheus server (adjust port as needed)
start_http_server(8000, registry=registry)

# Paths to your scripts
CAPTURE_SCRIPT = 'C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/capture/live_capture.py'  # Adjust this path if needed
DETECT_SCRIPT = 'C:/Users/lenovo/OneDrive/Desktop/Project 1/network-anomaly-new/detection/anomaly_detection.py'  # Adjust this path if needed

# State management for subprocess
if 'capture_process' not in st.session_state:
    st.session_state.capture_process = None

# Function to start packet capture
def start_capture():
    if st.session_state.capture_process is None:
        try:
            st.session_state.capture_process = subprocess.Popen(
                ["python", CAPTURE_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            st.success("Packet capture started.")
        except Exception as e:
            st.error(f"Failed to start capture: {e}")
    else:
        st.warning("Packet capture is already running.")

# Function to stop packet capture
def stop_capture():
    if st.session_state.capture_process is not None:
        try:
            st.session_state.capture_process.terminate()
            st.session_state.capture_process.wait()
            st.session_state.capture_process = None
            st.success("Packet capture stopped.")
        except Exception as e:
            st.error(f"Error stopping capture: {e}")
    else:
        st.warning("No active packet capture to stop.")

# Function to detect anomalies
def detect_anomalies():
    try:
        result = subprocess.run(["python", DETECT_SCRIPT], capture_output=True, text=True)
        st.text("Anomaly Detection Output:\n")
        st.code(result.stdout)
    except Exception as e:
        st.error(f"An error occurred during anomaly detection: {e}")

# Streamlit UI
st.title("Network Traffic Capture and Anomaly Detection")

# Buttons for capture and anomaly detection
if st.button("Start Capture"):
    start_capture()

if st.button("Stop Capture"):
    stop_capture()

if st.button("Detect Anomalies"):
    detect_anomalies()
