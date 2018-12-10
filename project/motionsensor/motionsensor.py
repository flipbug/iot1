import os
from paho.mqtt.publish import single
import grovepi

host = os.environ['MQTT_BROKER_IP']


# PIR sensor setup
pir = 2
grovepi.pinMode(pir, "INPUT")
armed = 1

while(True):
    try:
        if (grovepi.digitalRead(pir) == 1 and armed == 1):
            print("Motion detected. Sensor disarmed")
            single('megasec/motionsensor', payload='motion detected', hostname=host)
            armed = 0
        if (grovepi.digitalRead(pir) == 0 and armed == 0):
            print("No more motion. Sensor armed again")
            armed = 1
    except IOError:
        print("There was an I/O Error :(")