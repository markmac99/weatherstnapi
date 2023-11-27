#!/bin/bash

# copyright Mark McIntyre, 2023-

import time
import datetime
import os
import sys
import json
import paho.mqtt.client as mqtt

from mqConfig import readConfig, stationAltitude

from bme280 import bme280, bme280_i2c


def writeLogEntry(logdir, msg):
    with open(os.path.join(logdir, "bmp280-"+datetime.datetime.now().strftime("%Y%m%d")+".log"), mode='a+', encoding='utf-8') as f:
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
    client = mqtt.Client('bmp280_fwd')
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(broker, mqport, 60)
    for ele in data:
        topic = f'sensors/bmp280/{ele}'
        ret = client.publish(topic, payload=data[ele], qos=0, retain=False)
    writeLogEntry(logdir, f'sent {data}\n')
    return ret


def getTempPressHum():
    data = bme280.read_all()
    humidity, pressure, cTemp = data
    pressure = correctForAltitude(pressure, cTemp, stationAltitude())
    now = datetime.datetime.now().isoformat()[:19]+'Z'
    return {'temp_c_in': round(cTemp,2), 'press_rel': round(pressure,2), 'humidity_in': round(humidity,2), 'time': now}



def correctForAltitude(press, temp, alti):
    denom = temp + 273.15 + 0.0065 * alti
    val = (1 - (0.0065 * alti)/denom)
    press_sl = press * pow(val, -5.257)
    return round(press_sl,2)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        outdir = './maplinstn'
        logdir = './logs'
        stopfile = './stopbmp280' # to allow a clean stop from systemd
    else:
        outdir = os.path.join(sys.argv[1], 'maplinstn')
        logdir = os.path.join(sys.argv[1], 'logs')
        stopfile = os.path.join(sys.argv[1], 'stopbmp280')
    runme = True
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)
    outfname = os.path.join(outdir,'bmp280.json')
    bme280_i2c.set_default_i2c_address(0x76)
    bme280_i2c.set_default_bus(1)
    bme280.setup()
    while runme is True:
        data = getTempPressHum()
        with open(outfname, 'a+') as outf:
            outf.write(json.dumps(data) + '\n')
        sendDataToMQTT(data, logdir)
        time.sleep(60)
        if os.path.isfile(stopfile):
            writeLogEntry(logdir, 'Exiting...\n==========\n')
            os.remove(stopfile)
            runme = False
            break
