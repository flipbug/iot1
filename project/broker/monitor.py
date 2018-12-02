import os
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to megasec broker: " + str(rc))
    client.subscribe('#')

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

mqtt_broker_ip = os.environ['MQTT_BROKER_IP']
client.connect(mqtt_broker_ip, 1883, 60)

client.loop_forever()