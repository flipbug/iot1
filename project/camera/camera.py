import os
import paho.mqtt.client as mqtt
from PIL import Image
from dotenv import load_dotenv
import boto3

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

        if not HAS_CAMERA:
            self.image_file = "/Users/dpacassi/ZHAW/iot1/project/resources/image.jpg"

    # Rotate the image and save it as file.
    def rotate(self):
        image_object = Image.open(self.image_file)
        image_object = image_object.rotate(180)
        image_object.save(self.image_file)

    # Connect to the MQTT broker.
    def connect(self):
        mqtt_broker_ip = os.environ['MQTT_BROKER_IP']

        self.client.connect(mqtt_broker_ip, 1883, 60)
        self.client.loop_forever()

    # Upload our image to S3.
    def upload(self):
        s3 = boto3.resource('s3')
        data = open(self.image_file, 'rb')
        s3.Bucket(os.environ['S3_BUCKET']).put_object(Key='image.jpg', Body=data, ACL='public-read')

    # Capture an image.
    def capture_image(self):
        # Only use the camera resources when needed and don't
        # block it for other scripts.
        with picamera.PiCamera() as camera:
            # Capture image.
            camera.resolution = (1280, 720)
            camera.capture(self.image_file)

            # Rotate image.
            self.rotate()

            # Upload image to S3.
            self.upload()

    # on_connect(): Subscribe to our topic.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected to megasec broker: " + str(rc))
        self.client.subscribe('megasec/camera/make_picture')

    # on_message(): Actions to process when a message has been published to our subscribed topic.
    def on_message(self, client, userdata, msg):
        print("Capture image")
        self.capture_image()
        self.client.publish('megasec/camera/send_picture', payload="binary string")


if __name__ == "__main__":
    load_dotenv()
    camera = Camera()

    if HAS_CAMERA:
        if os.environ.get('MQTT_BROKER_IP') is not None:
            camera.connect()
        else:
            camera.capture_image()
    else:
        # We don't have a camera, simply upload our image.
        camera.upload()
