import requests

url = "http://localhost:5000/predict"
data = {
    "packet_size": 400,
    "protocol": "TCP"
}

response = requests.post(url, json=data)
print("Response:", response.status_code)
print("Data:", response.json())
