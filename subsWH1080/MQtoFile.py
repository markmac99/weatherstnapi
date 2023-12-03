# Copyright (c) Mark McIntyre, 2023-

# python code to save weatherstation data from MQ

import os
import sys
import json
import datetime
import paho.mqtt.client as mqtt

from mqConfig import readConfig


def writeLogEntry(msg):
    os.makedirs(logdir, exist_ok=True)
    with open(os.path.join(logdir, "readmq-"+datetime.datetime.now().strftime("%Y%m%d")+".log"), mode='a+', encoding='utf-8') as f:
        nowdt = datetime.datetime.now().isoformat()
        f.write('{}: {}\n'.format(nowdt, msg))


# The MQTT callback function. It will be triggered when trying to connect to the MQTT broker
def on_connect(client, userdata, flags, rc):
    client.subscribe([('sensors/wh1080/rain_mm',2),('sensors/bmp280/temp_c_in',2), 
                      ('sensors/bmp280/press_rel',2),('sensors/wh1080/wind_max_km_h',2),
                      ('sensors/wh1080/wind_avg_km_h',2),('sensors/wh1080/wind_dir_deg',2),
                      ('sensors/wh1080/temperature_C',2),('sensors/wh1080/humidity',2),
                      ('sensors/bmp280/humidity_in',2)])
    #writeLogEntry("subscription status " + str(x))
    if rc == 0:
        writeLogEntry("Connected success")
    else:
        writeLogEntry("Connected fail with code" + str(rc))


# the MQ subscribe callback
def on_subscribe(mosq, obj, mid, granted_qos):
    writeLogEntry("Subscribed: " + str(mid) + " " + str(granted_qos))
    return 


def on_disconnect(a,b,c):
    writeLogEntry("disconnected")


def on_message(mosq, obj, msg):
    lis = open(datafile,'r').readlines()
    olddata = json.loads(lis[0].strip())
    topic = os.path.split(msg.topic)[1]
    val = float(msg.payload.decode())
    olddata[topic] = val
    with open(datafile,'w') as outf:
        outf.write('{}'.format(json.dumps(olddata)))
    writeLogEntry(olddata)


if __name__=='__main__':
    global datafile
    global logdir
    dtstr = datetime.datetime.now().strftime('%Y%m%d')
    if len(sys.argv) < 2:
        outdir = '.'
        logdir = './logs'
    else:
        outdir = sys.argv[1]
        logdir = os.path.join(sys.argv[1], 'logs')
    broker, mqport = readConfig()
    writeLogEntry('===== Starting...')
    client = mqtt.Client('readweather', clean_session=False)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, mqport, 60)
    os.makedirs(outdir, exist_ok=True)
    datafile = os.path.join(outdir,'weatherdata.json')
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
    client.loop_forever(retry_first_connection=True)
