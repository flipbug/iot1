from grovepi import pinMode, digitalRead


class GrovePiButton:

    BUTTON_PIN = 2

    def __init__(self):
        pinMode(self.BUTTON_PIN, 'INPUT')

    def read(self):
        return digitalRead(self.BUTTON_PIN)