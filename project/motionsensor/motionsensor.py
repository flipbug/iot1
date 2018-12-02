import os
from paho.mqtt.publish import single

host = os.environ['MQTT_BROKER_IP']

single('megasec/motionsensor', payload='motion detected', hostname=host)