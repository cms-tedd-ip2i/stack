import paho.mqtt.client as mqtt
import json
import time

def on_connect(client, userdata, flags, rc):
    print(f"Ph2_ACF Simulator connected with result code {rc}")
    client.subscribe("ph2_acf/commands/#")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        fc7_id = payload.get('fc7_id', 'fc7_1')
        command = msg.topic.split('/')[-1]
        output_topic = f"ph2_acf/output/{fc7_id}"
        
        if command == "configure_fpga":
            client.publish(output_topic, f"Simulated: Starting upload of {payload.get('firmware_name')}...")
            time.sleep(2)
            client.publish(output_topic, f"Simulated: FC7 {fc7_id} configured successfully with {payload.get('xml_file')}")
        
        elif command == "lpgbt_id":
            client.publish(output_topic, f"Simulated: Running LPGBT ID test on {fc7_id}...")
            time.sleep(1)
            client.publish(output_topic, "Simulated: LPGBT ID Test PASSED")
            
    except Exception as e:
        print(f"Error processing command: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mosquitto", 1883, 60)

client.loop_forever()