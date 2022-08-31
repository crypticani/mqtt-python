##!/usr/bin/env python

import time
import threading
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

mqtt_topic = "client"

#######################################
# MQTT  server details
broker_addr = "192.168.101.113"
broker_port = 1883
topic_subscribe = mqtt_topic

#######################################
# Class that sends status //MQTT Reciver too
class run_mqtt(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    
    def run(self):   
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        try:
            
            client.connect(broker_addr, broker_port, 60)
            client.loop_start()
            
        except Exception as e:
            print(e)
            pass
      
def on_connect(client, userdata, flags, rc):
    try:
        client.subscribe(topic_subscribe)
    except Exception as e:
        print(e)
        pass
    
def on_message(client, userdata, msg):
    try:
        message = str(msg.payload.decode("utf-8"))
        print()
        print(message)
        print("------------------------------------------------------\n:", end="")
        
    except Exception as e:
        print(e)
        pass
    
    
def send(client, msg):
    try:
        publish.single(client, msg, hostname=broker_addr)
    except Exception as e:
        print(e)
        pass


run_mqtt()
print("Welcome to Mqtt-Linux Terminal.")
while True:
    time.sleep(1)
    data = input(">")
    client = topic_subscribe
    send(client,data)
    
