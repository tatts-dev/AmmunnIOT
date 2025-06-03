# simulator.py
import requests
import random
import time

URL = "http://localhost:5000/predict"

PROTOCOLS = ["TCP", "UDP", "ICMP"]


def simulate_packet():
    packet = {
        "packet_size": random.randint(20, 1500),  # Random packet size (bytes)
        "protocol": random.choice(PROTOCOLS),  # Random protocol
    }
    return packet


while True:
    packet = simulate_packet()
    try:
        response = requests.post(URL, json=packet)
        if response.status_code == 200:
            result = response.json()
            print(f"📦 Sent: {packet} → Anomaly: {result['anomaly']}")
        else:
            print("❌ Error:", response.text)
    except Exception as e:
        print("⚠️  Could not connect to API:", str(e))

    time.sleep(1)  # Wait 1 second before sending the next packet
