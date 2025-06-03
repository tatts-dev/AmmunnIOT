import pickle
import pandas as pd
from scapy.all import sniff, TCP, UDP

# Load the trained anomaly detection model
model = pickle.load(open("anomaly_model.pkl", "rb"))

def packet_callback(packet):
    # Extract packet size
    packet_size = len(packet)

    # Determine protocol (TCP=1, else=0)
    if packet.haslayer(TCP):
        protocol_encoded = 1
        protocol_name = "TCP"
    elif packet.haslayer(UDP):
        protocol_encoded = 0
        protocol_name = "UDP"
    else:
        # For other protocols, mark as 0 or handle differently
        protocol_encoded = 0
        protocol_name = "OTHER"

    # Create feature DataFrame for model input
    features = pd.DataFrame([[packet_size, protocol_encoded]], columns=["packet_size", "protocol"])

    # Predict anomaly (-1 means anomaly for IsolationForest)
    prediction = model.predict(features)

    if prediction[0] == -1:
        print(f"⚠️ Anomaly detected! Packet: size={packet_size}, protocol={protocol_name}")
    else:
        print(f"Normal packet: size={packet_size}, protocol={protocol_name}")

def main():
    print("Starting live traffic sniffing... Press Ctrl+C to stop.")
    # Sniff TCP and UDP packets only, call packet_callback on each
    sniff(filter="tcp or udp", prn=packet_callback, store=False)

if __name__ == "__main__":
    main()
