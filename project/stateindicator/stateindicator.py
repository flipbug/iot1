import os
import threading
import paho.mqtt.client as mqtt

from grovepi_led import GrovePiLed


class StateIndicator:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # self.client.tls_set(ca_certs="/etc/ssl/certs/ca.crt", tls_version=2)
        self.blink = False
        self.led = GrovePiLed()

    def run(self):
        mqtt_broker_ip = os.environ['MQTT_BROKER_IP']

        self.client.connect(mqtt_broker_ip, 1883, 60)

        # Use non-blocking mqtt loop for buzzing
        while True:
            self.client.loop()
            if self.blink:
                self.led.blink()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to megasec broker: " + str(rc))
        self.client.subscribe('megasec/state')

    def on_message(self, client, userdata, msg):
        print("Message received: " + msg.payload)

        self.blink = False
        if msg.payload == b'SleepState':
            self.led.off()
        elif msg.payload == b'ActiveState':
            self.led.on()
        elif msg.payload == b'TriggeredState':
            self.blink = True
 

if __name__ == "__main__":
    indicator = StateIndicator()
    indicator.run()