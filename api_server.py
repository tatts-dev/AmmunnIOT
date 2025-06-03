from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time
import random
import pickle
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load your trained IsolationForest model
model = pickle.load(open("anomaly_model.pkl", "rb"))

# Sample hospital IoT devices with MAC addresses
devices = [
    {"device_name": "Heart Monitor A1", "mac_address": "00:1A:C2:7B:00:01"},
    {"device_name": "Infusion Pump B2", "mac_address": "00:1A:C2:7B:00:02"},
    {"device_name": "Ventilator C3", "mac_address": "00:1A:C2:7B:00:03"},
    {"device_name": "MRI Scanner D4", "mac_address": "00:1A:C2:7B:00:04"},
    {"device_name": "Oxygen Sensor E5", "mac_address": "00:1A:C2:7B:00:05"}
]

# Global dictionary to hold the latest packet and prediction
latest_packet = {
    "device_name": None,
    "mac_address": None,
    "packet_size": None,
    "protocol": None,
    "anomaly": None
}

def simulate_packet():
    """
    Generate a random IoT packet with device metadata
    """
    device = random.choice(devices)
    packet_size = random.choice([50, 100, 200, 400, 800, 1500])
    protocol = random.choice(["TCP", "UDP"])
    return device["device_name"], device["mac_address"], packet_size, protocol

def predict_anomaly(packet_size, protocol):
    protocol_encoded = 1 if protocol.upper() == "TCP" else 0
    features = pd.DataFrame([[packet_size, protocol_encoded]], columns=["packet_size", "protocol_num"])
    prediction = model.predict(features)
    return bool(prediction[0] == -1)

def background_traffic_simulation():
    global latest_packet
    while True:
        device_name, mac_address, packet_size, protocol = simulate_packet()
        anomaly = predict_anomaly(packet_size, protocol)

        latest_packet = {
            "device_name": device_name,
            "mac_address": mac_address,
            "packet_size": packet_size,
            "protocol": protocol,
            "anomaly": anomaly
        }

        print(f"Simulated: {device_name} | {mac_address} | {packet_size} bytes | {protocol} | {'Anomaly ❗' if anomaly else 'Normal ✅'}")
        time.sleep(3)

@app.route("/")
def home():
    return "<h2>✅ MedAegis AI API is running</h2><p>Use GET /latest to get latest simulated packet with anomaly detection.</p>"

@app.route("/latest")
def get_latest():
    if latest_packet["packet_size"] is None:
        return jsonify({"error": "No data yet"}), 503
    return jsonify(latest_packet)

if __name__ == "__main__":
    # Start background thread
    thread = threading.Thread(target=background_traffic_simulation, daemon=True)
    thread.start()

    app.run(debug=True)





