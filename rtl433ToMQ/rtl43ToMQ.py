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
import math
import paho.mqtt.client as mqtt

from mqConfig import readConfig


def writeLogEntry(logdir, msg):
    with open(os.path.join(logdir, "WH1080Fwd-"+datetime.datetime.now().strftime("%Y%m%d")+".log"), mode='a+', encoding='utf-8') as f:
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


def sendDataToMQTT(data, logdir):
    broker, mqport = readConfig()
    client = mqtt.Client('wh1080_fwd')
    client.on_connect = on_connect
    client.on_publish = on_publish
    try:
        client.connect(broker, mqport, 60)
    except Exception as e:
        print(e)
        writeLogEntry(logdir, 'Unable to connect to MQ - will try again shortly\n')
        return 0
    for ele in data:
        topic = f'sensors/wh1080/{ele}'
        ret = client.publish(topic, payload=data[ele], qos=0, retain=False)
    writeLogEntry(logdir, 'sent data\n')
    return ret


def windChill(t, v):
    wc = 13.12 + 0.6215 * t -11.37 * pow(v, 0.16) + 0.3965 * t * pow(v, 0.16)
    return round(wc,4)


def heatIndex(t, rh):
    c_1 = -8.78469475556
    c_2 = 1.61139411
    c_3 = 2.33854883889
    c_4 = -0.14611605
    c_5 = -0.012308094
    c_6 = -0.016425
    c_7 = 2.211732e-3
    c_8 = 7.2546e-4
    c_9 = -3.582e-6
    HI =c_1 + c_2 * t + c_3 * rh + c_4 * t*rh +c_5 * t*t + \
        c_6 * rh*rh + c_7 * t*t*rh + c_8 *t *rh*rh +c_9*t*t * rh*rh
    return round(HI,4)


def dewPoint(t, rh): 
    # t in C, rh as a number eg 90, 50
    E0 = 0.611 # kPa
    lrv = 5423 # K (L/Rv over flat surface of water)
    T0 = 273.15 # K
    Es = E0 * math.exp(lrv * (1/T0 - 1/(t + T0)))
    dewPoint = 1.0 / (-math.log(rh/100 * Es/E0)/lrv + 1/T0)-T0
    return round(dewPoint,4)


def jsonToMQ(fname, priordata, logdir):
    lis = open(fname, 'r').readlines()
    lastline = lis[-1].strip()
    if lastline[-6:] != '"CRC"}':
        writeLogEntry(logdir, f'malformed line {lastline}\n')
        return 
    else:
        if lastline == priordata:
            writeLogEntry(logdir, f'data unchanged {lastline}\n')
            return lastline
        eles = json.loads(lastline)
        t = eles['temperature_C']
        v = eles['wind_avg_km_h']
        h = eles['humidity']
        eles['feels_like'] = t
        wc = windChill(t, v)
        hi = heatIndex(t, h)
        if wc < t:
            eles['feels_like'] = wc
        elif t > 26 and hi > t:
            eles['feels_like'] = hi
        eles['dew_point'] = dewPoint(t, h)
        sendDataToMQTT(eles, logdir)
    return lastline


if __name__=='__main__':
    fname = sys.argv[1]
    logdir = os.path.join(sys.argv[2], 'logs')
    stopfile = os.path.join(sys.argv[2], 'stopwhfwd')
    writeLogEntry(logdir, '=====\nStarting...\n')
    runme = True
    prevdata={}
    while runme is True:
        if os.path.isfile(fname):
            prevdata = jsonToMQ(fname, prevdata, logdir)
        else:
            writeLogEntry(logdir, 'datafile not found\n')
        time.sleep(60)
        if os.path.isfile(stopfile):
            writeLogEntry(logdir, 'Exiting...\n=====')
            os.remove(stopfile)
            runme = False
            break
