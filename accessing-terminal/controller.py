##!/usr/bin/env python
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import random
import time
import threading
import socket,subprocess


#######################################
# -------------------------------------------------
#
# MQTT  server details
# ------------------------------------------------
#######################################
broker_addr = "192.168.101.113"
broker_port = 1883
topic_publish_status = "bd/status"
# toipc_publish_result = "bd/listen"
topic_subscribe = "bd/result"
live_interval = 5
#######################################
#---------------------------------------------------
#
# Class that sends status //MQTT Reciver too
#
#---------------------------------------------------
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
            
            # Blocking call that processes network traffic, dispatches callbacks and
            # handles reconnecting.
            # Other loop*() functions are available that give a threaded interface and a
            # manual interface.
            client.loop_start()
            
        except Exception as e:
            print(e)
            pass
      
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    try:
        client.subscribe(topic_subscribe)
    except Exception as e:
        print(e)
        pass
    # The callback for when a PUBLISH message is received from the server.
    
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
    data = input(":")
    client = "user2"
    send(client,data)
    