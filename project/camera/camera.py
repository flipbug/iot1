import os
import paho.mqtt.client as mqtt
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from dotenv import load_dotenv
import boto3
from datetime import datetime

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
        self.image_width = 1280
        self.image_height = 720
        self.capture_file = "/home/pi/iot1/project/resources/capture.jpg"
        self.snapshot_file = "/home/pi/iot1/project/resources/snapshot.png"
        self.ttf_file = "/home/pi/iot1/project/camera/RobotoMono-Regular.ttf"

        if not HAS_CAMERA:
            self.capture_file = "/Users/dpacassi/ZHAW/iot1/project/resources/capture.jpg"
            self.snapshot_file = "/Users/dpacassi/ZHAW/iot1/project/resources/snapshot.png"
            self.ttf_file = "/Users/dpacassi/ZHAW/iot1/project/camera/RobotoMono-Regular.ttf"

    # Rotate the image and save it as file.
    def rotate(self):
        image_object = Image.open(self.capture_file)
        image_object = image_object.rotate(180)
        image_object.save(self.capture_file)

    # Connect to the MQTT broker.
    def connect(self):
        mqtt_broker_ip = os.environ['MQTT_BROKER_IP']

        self.client.connect(mqtt_broker_ip, 1883, 60)
        self.client.loop_forever()

    # Create and upload our snapshot to S3.
    def upload(self):
        # Prepare snapshot.
        padding = 8
        text = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        img = Image.open(self.capture_file)
        font = ImageFont.truetype(self.ttf_file, 24)
        text_size = font.getsize(text)
        button_img = Image.new('RGBA', (text_size[0] + padding * 2, text_size[1] + padding), "black")
        button_draw = ImageDraw.Draw(button_img)
        button_draw.text((padding, 0), text, (0, 255, 0), font=font)
        img.paste(button_img, (self.image_width - text_size[0] - padding * 2, self.image_height - text_size[1] - padding))
        img.save(self.snapshot_file)

        # Upload capture and snapshot.
        s3 = boto3.resource('s3')
        data = open(self.capture_file, 'rb')
        s3.Bucket(os.environ['S3_BUCKET']).put_object(Key='capture.jpg', Body=data, ACL='public-read')
        data = open(self.snapshot_file, 'rb')
        s3.Bucket(os.environ['S3_BUCKET']).put_object(Key='snapshot.png', Body=data, ACL='public-read')

    # Capture an image.
    def capture_image(self):
        # Only use the camera resources when needed and don't
        # block it for other scripts.
        with picamera.PiCamera() as camera:
            # Capture image.
            camera.resolution = (self.image_width, self.image_height)
            camera.capture(self.capture_file)

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
        print("Capture image, timestamp: " + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
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
