# MQTT - Python
MQTT - Message Queue Telemetry Protocol

## Setup
- Install mosquitto broker:
    `apt-get install mosquitto mosquitto-clients`

- Install mqtt:
    `pip install -r requirements.txt`

## Using mqtt to run commands on multiple clients
- It is achieved using Publish and Subscribe

### To differentiate different clients
- give a unique name to topic subscribe in client's file
- change publishing topic as the unique name of client 