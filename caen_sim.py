import paho.mqtt.client as mqtt
import json
import time
import random

def on_connect(client, userdata, flags, rc):
    print(f"CAEN Simulator connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("mosquitto", 1883, 60)

slots = [12, 13, 14, 15] # Mimicking slots seen in your Grafana dashboards

while True:
    data = []
    for slot in slots:
        for chan in range(12):
            data.append({
                "slot": str(slot),
                "number": str(chan),
                "vreq": random.uniform(0, 500) if random.random() > 0.1 else 0.0,
                "ireq": random.uniform(0, 100),
                "status": 1 if random.random() > 0.05 else 8 # Mostly 'ON', occasionally 'ALARM'
            })
    
    client.publish("/SY4527/status", json.dumps(data))
    print("Published fake CAEN status")
    time.sleep(5)