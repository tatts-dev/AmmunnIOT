import time
import random
import pickle
import pandas as pd

# Load your trained model
model = pickle.load(open("anomaly_model.pkl", "rb"))

# Global variable to hold latest packet info
latest_packet = {}

# Sample hospital IoT devices
devices = [
    {"name": "Heart Monitor A1", "mac": "00:1A:C2:7B:00:01"},
    {"name": "Infusion Pump B2", "mac": "00:1A:C2:7B:00:02"},
    {"name": "Ventilator C3", "mac": "00:1A:C2:7B:00:03"},
    {"name": "MRI Scanner D4", "mac": "00:1A:C2:7B:00:04"}
]

def predict_packet(packet_size, protocol):
    protocol_encoded = 1 if protocol == "TCP" else 0
    features = pd.DataFrame([[packet_size, protocol_encoded]], columns=["packet_size", "protocol_num"])
    prediction = model.predict(features)
    return prediction[0]

def generate_random_packet():
    device = random.choice(devices)
    packet_size = random.choice([50, 100, 200, 400, 800, 1500])
    protocol = random.choice(["TCP", "UDP"])
    return device["name"], device["mac"], packet_size, protocol

def main():
    global latest_packet
    print("Starting simulated hospital IoT traffic anomaly detection...\n")

    while True:
        device_name, mac, size, proto = generate_random_packet()
        pred = predict_packet(size, proto)

        latest_packet = {
            "device_name": device_name,
            "mac_address": mac,
            "packet_size": size,
            "protocol": proto,
            "anomaly": pred == -1
        }

        status = "❗ Anomaly Detected" if latest_packet["anomaly"] else "✅ Normal"
        print(f"{device_name} | {mac} | Size: {size} | {proto} --> {status}")

        time.sleep(2)

if __name__ == "__main__":
    main()


