import os
import time
from paho.mqtt.publish import single
from virtual_button import VirtualButton


class ToggleSwitch:
    def __init__(self):
        self.mqtt_broker_ip = os.environ['MQTT_BROKER_IP']
        self.tls_conf = {"ca_certs": "/etc/ssl/certs/ca.crt"}
        self.tls_conf = None

        self.init_button()

    def init_button(self):
        if os.environ.get('VIRTUAL', False):
            self.button = VirtualButton()
        else:
            # import locally to prevent dependency issues with grove pi
            from grovepi_button import GrovePiButton
            self.button = GrovePiButton()

    def run(self):
        button_press = False 
        while True:
            button_status = self.button.read()
            if button_status and not button_press:
                print('Button Press')
                button_press = True
                self.send_message()
            elif not button_status:
                button_press = False

    def send_message(self):
        single('megasec/toggleswitch', 
        payload='pressed', 
        hostname=self.mqtt_broker_ip,
        port=1883,
        tls=self.tls_conf)
   

if __name__ == "__main__":
    toggleswitch = ToggleSwitch()
    toggleswitch.run()