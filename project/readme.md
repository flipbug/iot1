# IoT1 - Project

This application implements a distributed home surveillance system using MQTT. 

## Setup

### Using the dev setup

Each node is available as a docker container for easier development and testing. Start by running `docker-compose up`.

Use the toggle switch:
```
docker-compose run toggleswitch python toggleswitch.py 
```

Monitor traffic:
```
docker-compose exec broker python monitor.py 
```

## Architecture

insert fancy diagram

## Hardware

* 3x raspberry pi
* 1x button
* 1x camera
* 1x motiondetector

## Project Deliverables:

Presuming most laboratories are done in groups there will be an “abnahme” of about 10’ demonstration demonstrating an application-based awareness of system characteristics, including, but not necessarily limited to:

* Residence of application
* Relationship to time
* Relationship to location
* Discovery and identification
* Verification and validation
* Long term storage of data
* Error handling
* Lessons learned 
