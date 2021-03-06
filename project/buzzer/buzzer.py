import os
import threading
import paho.mqtt.client as mqtt

from grovepi_buzzer import GrovePiBuzzer


class Buzzer:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # self.client.tls_set(ca_certs="/etc/ssl/certs/ca.crt", tls_version=2)
        self.alarm_active = False
        self.buzzer = GrovePiBuzzer()

    def run(self):
        mqtt_broker_ip = os.environ['MQTT_BROKER_IP']

        self.client.connect(mqtt_broker_ip, 1883, 60)

        # Use non-blocking mqtt loop for buzzing
        while True:
            self.client.loop()
            if self.alarm_active:
                self.buzzer.buzz()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to megasec broker: " + str(rc))
        self.client.subscribe('megasec/alarm')

    def on_message(self, client, userdata, msg):
        print("Message received: " + msg.topic)

        if msg.payload == b'active':
            self.alarm_active = True
        elif msg.payload == b'inactive':
            self.alarm_active = False
 

if __name__ == "__main__":
    buzzer = Buzzer()
    buzzer.run()