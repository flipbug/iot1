# File:   control_loop_template.py
# Author: leiu
#         masd

import signal
import json
import urllib
from urllib.request import urlopen
import codecs
from time import sleep

LESHAN_SERVER_IP = "172.16.32.5"
LESHAN_SERVER_PORT = "8080"

CLIENT_1_NAME = "iot-pi-right-front"
CLIENT_2_NAME = "iot-pi-left-front"

# Add additional IoT client names here if needed
# ################################################

# ################################################

BASE_URL = "http://" + LESHAN_SERVER_IP + ":" + LESHAN_SERVER_PORT + \
           "/api/clients"

SLEEP_TIME = float(0.7)  # unit is seconds

# Example URL concatenations ...
URL_ROTARY_ANGLE_SENSOR = BASE_URL + "/" + CLIENT_1_NAME + "/3202/0/5600"

URL_LED = BASE_URL + "/" + CLIENT_2_NAME + "/3201/0/5550"

# Add additional resources here if needed
# #############################################

# #############################################


running = True


def signal_handler(*args):
  print('Got SIGINT, cleaning up and exiting ...')
  global running
  running = False


def example_get(url):
  reader = codecs.getreader('utf8')
  # change response from byte to string
  data = json.load(reader(urlopen(url)))
  return data


def example_put(value, url, resource_id):
  json_data = {}
  json_data['id'] = resource_id
  json_data['value'] = value

  json_string = json.dumps(json_data)

  opener = urllib.request.build_opener(urllib.request.HTTPHandler)
  request = urllib.request.Request(url, data=json_string.encode('utf8'))
  request.add_header('Content-Type', 'application/json')
  request.get_method = lambda: 'PUT'
  url = opener.open(request)


def main():
  signal.signal(signal.SIGINT, signal_handler)

  # Find Resource example ...
  print("Get source tree \n")
  print(BASE_URL)
  source_tree = example_get(BASE_URL)
  print(json.dumps(source_tree, indent=4, sort_keys=True))
  print("\n")
  source_tree_client = example_get(BASE_URL + "/" + CLIENT_1_NAME)
  print(json.dumps(source_tree_client, indent=4, sort_keys=True))
  print("\n")
  source_tree_ressource = example_get(BASE_URL + "/" + CLIENT_1_NAME + "/3202")
  print(json.dumps(source_tree_ressource, indent=4, sort_keys=True))
  print("\n")
  source_tree_ressource = example_get(BASE_URL + "/" + CLIENT_1_NAME + "/3201")
  print(json.dumps(source_tree_ressource, indent=4, sort_keys=True))
  print("\n")
  # ##########################################################################

  print("Entering Control Loop")

  while running:
    # Example for retrieving data from a rotary angle sensor
    data = example_get(URL_ROTARY_ANGLE_SENSOR)
    print(data['content']['value'])
    sensor_value = (data['content']['value'])

    # Write your code here. Values can be sent
    # towards actuators with the example_put function
    # #############################################

    # #############################################

    sleep(SLEEP_TIME)


if __name__ == "__main__":
  main()
