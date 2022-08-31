##!/usr/bin/env python

import time
import threading
import subprocess
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

mqtt_id = ""
with open("/etc/mqtt-id", "r") as f:
    mqtt_id = f.read().replace("\n", "")

#######################################
# MQTT  server details
broker_addr = "192.168.101.113"
broker_port = 1883
topic_publish_status = "client/status"
topic_publish_result = "client/result"
topic_subscribe = mqtt_id
live_interval = 30

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
            while True:
                global live_interval
                
                proc = subprocess.Popen("ip a | grep wl | grep inet", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                # read output
                ip = str(proc.stdout.read().decode("utf-8")) + str(proc.stderr.read().decode("utf-8"))

                if ip is not None:
                    ip = ip.split()
                    ip = ip[1].split("/")
                else:
                    proc = subprocess.Popen("ip a | grep eth | grep inet", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    # read output
                    ip = str(proc.stdout.read().decode("utf-8")) + str(proc.stderr.read().decode("utf-8"))
                    ip = ip.split()
                    ip = ip[1].split("/")

                ip = "".join(ip[0])
                message = mqtt_id+" "+ip

                send(message,topic_publish_status)
                time.sleep(live_interval)
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
        message = str(msg.payload.decode('utf-8'))
        # print(message)
        proc = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # read output
        stdout_value = str(proc.stdout.read().decode("utf-8")) + str(proc.stderr.read().decode("utf-8"))
        
        send(str(stdout_value),topic_publish_result)
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
    time.sleep(0.05)
    pass
    
