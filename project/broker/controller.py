import os
import threading
import paho.mqtt.client as mqtt

from events import Event
from states import *


class Controller:

    TRIGGER_ALARM_DELAY = 30

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.current_state = SleepState()

    def run(self):
        mqtt_broker_ip = os.environ['MQTT_BROKER_IP']

        self.client.connect(mqtt_broker_ip, 1883, 60)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to megasec broker: " + str(rc))
        self.client.subscribe('megasec/#')

    def on_message(self, client, userdata, msg):
        print("Message received: " + msg.topic)
        event = None

        if msg.topic == 'megasec/toggleswitch':
            event = self.handle_toggleswitch(msg)

        if msg.topic == 'megasec/motionsensor':
            event = self.handle_motionsensor(msg)

        if msg.topic == 'megasec/camera/send_picture':
            # The camera does not influcene the state.
            self.handle_camera(msg)

        self.current_state = self.current_state.on_event(event)

    def handle_toggleswitch(self, msg):
        if isinstance(self.current_state, SleepState):
            event = Event.activate
        else:
            event = Event.deactivate
        
        print("Event: " + str(event))
        return event

    def handle_motionsensor(self, msg):
        if isinstance(self.current_state, ActiveState) and msg.payload == b'motion detected':
            event = Event.motion_detected
            self.client.publish('megasec/camera/make_picture', payload="test")

            # Start timer after which the alarm will be triggered if not deactivated first.
            threading.Timer(self.TRIGGER_ALARM_DELAY, self.tigger_timeout).start()

            print("Event: " + str(event))
            return event

    def handle_camera(self, msg):
        print("Picture received")

    def tigger_timeout(self):
        print("Trigger timeout received")
        self.current_state = self.current_state.on_event(Event.timeout)

        if isinstance(self.current_state, AlarmState):
            print("Send alarm")
            self.client.publish('megasec/alarm', payload="active")

 
if __name__ == "__main__":
    controller = Controller()
    controller.run()