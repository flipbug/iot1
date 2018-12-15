import time
from grovepi import pinMode, digitalWrite


class GrovePiBuzzer:

    BUZZER_PIN = 3
    SLEEP_INTERVAL = 0.5

    def __init__(self):
        pinMode(self.BUZZER_PIN, 'OUTPUT')

    def __del__(self):
        digitalWrite(self.BUZZER_PIN, 0)

    def buzz(self):
        digitalWrite(self.BUZZER_PIN, 1)
        time.sleep(self.SLEEP_INTERVAL)
        digitalWrite(self.BUZZER_PIN, 0)
