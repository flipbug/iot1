import os
from paho.mqtt.publish import single
import grovepi

host = os.environ['MQTT_BROKER_IP']


# PIR sensor setup
buzzer = 3
grovepi.pinMode(pir, "OUTPUT")

grovepi.digitalWrite(3, 1)