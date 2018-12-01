import os
from paho.mqtt.publish import single

host = os.environ['MQTT_BROKER_IP']

single('megasec/toggleswitch', payload='True', hostname=host)