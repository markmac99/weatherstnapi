# Copyright (c) Mark McIntyre, 2023-

# python code to save weatherstation data from MQ

import os
import sys
import json
import datetime
import paho.mqtt.client as mqtt


LOG_DIRECTORY = 'logs' 
STOPFILE = './stopreadmq' # to allow a clean stop from systemd
SLEEP_TIME = 60 # secods 


def writeLogEntry(msg):
    os.makedirs(LOG_DIRECTORY, exist_ok=True)
    with open(os.path.join(LOG_DIRECTORY,"readmq-"+datetime.datetime.now().strftime("%Y%m%d")+".log"), mode='a+', encoding='utf-8') as f:
        nowdt = datetime.datetime.now().isoformat()
        f.write('{}: {}\n'.format(nowdt, msg))


# The MQTT callback function. It will be triggered when trying to connect to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        writeLogEntry("Connected success")
    else:
        writeLogEntry("Connected fail with code", rc)


# the MQ publish function
def on_subscribe(mosq, obj, mid, granted_qos):
    writeLogEntry("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(mosq, obj, msg):
    datafile = os.path.join(outfdir,'weatherdata.json')
    lis = open(datafile,'r').readlines()
    olddata = json.loads(lis[0].strip())
    topic = os.path.split(msg.topic)[1]
    val = float(msg.payload.decode())
    olddata[topic] = val
    writeLogEntry('{} {}'.format(msg.topic, olddata))
    with open(datafile,'w') as outf:
        outf.write('{}'.format(json.dumps(olddata)))


if __name__=='__main__':
    global outfdir
    outfdir = sys.argv[1]
    broker = 'wxsatpi'
    mqport = 1883
    writeLogEntry('=====\nStarting...\n')
    client = mqtt.Client('readweather')
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(broker, mqport, 60)
    datafile = os.path.join(outfdir,'weatherdata.json')
    try: 
        lis = open(datafile,'r').readlines()
        data = json.loads(lis[0].strip())
    except:
        data = {'temp_c_in': 0, 'press_rel':0, 'wind_max_km_h':0, 'rain_mm':0,
            'wind_avg_km_h':0, 'wind_dir_deg':0, 'temperature_C':0,'humidity':0,
            'humidity_in':0}
        with open(datafile, 'w') as outf:
            outf.write('{}'.format(json.dumps(data)))

    client.subscribe([('sensors/wh1080/rain_mm',2),('sensors/bmp280/temp_c_in',2), 
                      ('sensors/bmp280/press_rel',2),('sensors/wh1080/wind_max_km_h',2),
                      ('sensors/wh1080/wind_avg_km_h',2),('sensors/wh1080/wind_dir_deg',2),
                      ('sensors/wh1080/temperature_C',2),('sensors/wh1080/humidity',2),
                      ('sensors/bmp280/humidity_in',2)])
    client.loop_forever()
