import os
import paho.mqtt.client as mqtt
from PIL import Image
from dotenv import load_dotenv

HAS_CAMERA = True

try:
  import picamera
except OSError:
  HAS_CAMERA = False

class Camera:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.image_file = "/home/pi/iot1/project/resources/image.jpg"

    def rotate(self):
        image_object = Image.open(self.image_file)
        image_object = image_object.rotate(180)
        image_object.save(self.image_file)

    def run(self):
        mqtt_broker_ip = os.environ['MQTT_BROKER_IP']

        self.client.connect(mqtt_broker_ip, 1883, 60)
        self.client.loop_forever()

    def devRun(self):
        # Only use the camera resources when needed and don't
        # block it for other scripts.
        with picamera.PiCamera() as camera:
            camera.resolution = (1280, 720)
            camera.capture(self.image_file)
            self.rotate()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to megasec broker: " + str(rc))
        self.client.subscribe('megasec/camera/make_picture')

    def on_message(self, client, userdata, msg):
        print("send picture")
        self.client.publish('megasec/camera/send_picture', payload="binary string")


if __name__ == "__main__":
    load_dotenv()

    if HAS_CAMERA:
        camera = Camera()

        if os.environ.get('MQTT_BROKER_IP') is not None:
            camera.run()
        else:
            camera.devRun()
