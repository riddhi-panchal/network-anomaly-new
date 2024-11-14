import streamlit as st
import subprocess
import os
import time
import pandas as pd

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
        st.text("Anomaly Detection Output:")
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
