# anomaly_model.py
from sklearn.ensemble import IsolationForest
import pandas as pd
import pickle
import numpy as np

# Simulate training data
data = {
    "packet_size": np.random.randint(50, 1000, 200),
    "protocol_num": np.random.randint(0, 3, 200),  # TCP: 0, UDP: 1, ICMP: 2
}
df = pd.DataFrame(data)

model = IsolationForest(contamination=0.1)
model.fit(df)

with open("anomaly_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved.")
