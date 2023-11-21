# Copyright (c) Mark McIntyre, 2023-

# python code to post weatherstation data to MQ
# unfortunately my weatherstation's USB port is broken, and even more frustratingly
# rtl_433 can't connect to MQ on my Pi3, so i have set it to write to CSV
# and this code reads from the CSV and posts to MQ

import datetime
import time
import os
import json
import sys
import paho.mqtt.client as mqtt


LOG_DIRECTORY = './logs/' 
STOPFILE = './stopwhfwd' # to allow a clean stop from systemd
SLEEP_TIME = 60 # secods 


def writeLogEntry(msg):
    with open(LOG_DIRECTORY+"WH1080Fwd-"+datetime.datetime.now().strftime("%Y%m%d")+".log", mode='a+', encoding='utf-8') as f:
        nowdt = datetime.datetime.now().isoformat()
        f.write(f'{nowdt}: {msg}')


# The MQTT callback function. It will be triggered when trying to connect to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print("Connected fail with code", rc)


# the MQ publish function
def on_publish(client, userdata, result):
    #print('data published - {}'.format(result))
    return


def sendDataToMQTT(data):
    broker = 'themcintyres.ddns.net'
    mqport = 9883
    client = mqtt.Client('wh1080_fwd')
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(broker, mqport, 60)
    for ele in data:
        topic = f'sensors/wh1080/{ele}'
        ret = client.publish(topic, payload=data[ele], qos=0, retain=False)
    writeLogEntry('sent data\n')
    return ret


def csvToMQ(fname, priordata):
    lis = open(fname,'r').readlines()
    lastline = lis[-1].strip()
    if lastline[-6:] != '"CRC"}':
        print('malformed line')
        return 
    else:
        if lastline == priordata:
            writeLogEntry('data unchanged\n')
            return lastline
        eles = json.loads(lastline)
        sendDataToMQTT(eles)
    return lastline


if __name__=='__main__':
    writeLogEntry('=====\nStarting...\n')
    fname = sys.argv[1]
    runme = True
    prevdata={}
    while runme is True:
        prevdata = csvToMQ(fname, prevdata)
        time.sleep(SLEEP_TIME)
        if os.path.isfile(STOPFILE):
            writeLogEntry('Exiting...\n=====')
            os.remove(STOPFILE)
            runme = False
            break
