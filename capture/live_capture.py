import subprocess
import os
import signal
import platform
import time

# Global variable to hold the subprocess reference
capture_process = None
fl = False  # Flag to indicate if capturing is active

def start_capture():
    global capture_process, fl
    # Ensure the 'data' directory exists
    if not os.path.exists('./data'):
        os.makedirs('./data')

    # File path for the output CSV
    file_path = "./data/live_traffic.csv"

    # Define the tshark command to capture the necessary fields
    tshark_command = [
        "tshark", "-i", "5", "-T", "fields",
        "-e", "frame.time_epoch",  # Epoch time of the frame
        "-e", "ip.src",            # Source IP address
        "-e", "ip.dst",            # Destination IP address
        "-e", "frame.len",         # Frame length
        "-e", "tcp.port",          # TCP port
        "-e", "udp.port",          # UDP port
        "-e", "ip.proto",          # Protocol type (e.g., TCP, UDP)
        "-e", "frame.time_delta",  # Duration (time between packets)
        "-e", "tcp.flags",         # TCP flags (such as SYN, ACK, etc.)
        "-e", "ip.len",            # Length of the IP packet
        "-e", "icmp.type",         # ICMP packet type (if relevant)
        "-e", "tcp.stream",        # TCP stream identifier
        "-e", "tcp.seq",           # TCP sequence number
        "-e", "tcp.ack",           # TCP acknowledgment number
        "-e", "ip.flags.df",       # Don't fragment flag
        "-e", "tcp.window_size",   # TCP window size
        "-e", "ip.ttl",            # Time to live
        "-e", "tcp.analysis.flags",# TCP analysis flags
        "-e", "http.request.uri",  # HTTP request URI (if applicable)
        "-e", "http.response.code",# HTTP response code (if applicable)
        "-E", "header=y",          # Include header in the output
        "-E", "separator=,",       # Use comma separator
        "-E", "quote=d",           # Use double quotes for field values
    ]

    try:
        # Start the tshark command as a subprocess
        if platform.system() == "Windows":
            capture_process = subprocess.Popen(
                tshark_command, stdout=open(file_path, 'w'), stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            capture_process = subprocess.Popen(
                tshark_command, stdout=open(file_path, 'w'), stderr=subprocess.PIPE, preexec_fn=os.setsid
            )
        fl = True
        print("Traffic capture started.")
    except Exception as e:
        print(f"Error during traffic capture: {e}")

def stop_capture():
    global capture_process, fl
    if capture_process is not None and fl:
        try:
            # Send a termination signal to the process group
            if platform.system() == "Windows":
                capture_process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                os.killpg(os.getpgid(capture_process.pid), signal.SIGTERM)
            capture_process.wait()  # Wait for the process to fully terminate
            print("Traffic capture stopped.")
        except Exception as e:
            print(f"Error stopping capture: {e}")
        finally:
            capture_process = None
            fl = False
    else:
        print("No active capture process to stop.")

if __name__ == "__main__":
    try:
        start_capture()
        time.sleep(15)  # Capture packets for 15 seconds
        stop_capture()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Stopping capture...")
        stop_capture()
