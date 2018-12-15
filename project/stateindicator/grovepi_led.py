import time
from grovepi import pinMode, digitalWrite


class GrovePiLed:

    LED_PIN = 5
    SLEEP_INTERVAL = 0.5

    def __init__(self):
        pinMode(self.LED_PIN, 'OUTPUT')

    def __del__(self):
        digitalWrite(self.LED_PIN, 0)

    def on(self):
        digitalWrite(self.LED_PIN, 1)

    def off(self):
        digitalWrite(self.LED_PIN, 0)

    def blink(self):
        digitalWrite(self.LED_PIN, 1)
        time.sleep(self.SLEEP_INTERVAL)
        digitalWrite(self.LED_PIN, 0)