# -*- coding: utf-8 -*-
"""
Script to collect data from WeatherUnderground
Still needs some work to handle errors

"""
import requests
import json
import threading
import time
from datetime import datetime
from openhab import OpenHAB
import os

from wuconfig import stationid, getWUkey, getOpenhabURL

import backoff

BASE_URL = 'https://api.weather.com/'
LIVEDATA_URL = 'v2/pws/observations/current?' 
LOG_DIRECTORY = './logs/'
num_max_retries = 20
sleep_time = 60 # wunderground limits you to 1500 requests per day = 1 per min


@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=5,
    giveup=lambda e: e.response is not None and e.response.status_code < 500
)
class WuData(threading.Thread):

    def __init__(self, stationid, apikey):

        self.writeLogEntry("Start Intalising: " + str(datetime.now()))
        threading.Thread.__init__(self)
        #super(Thread, self).__init__()
        self._stop = threading.Event()
        self.sid = stationid
        self.key = apikey
        self.headers = ""
        self.deviceId = ""
        self.writeLogEntry("End Intalising: " + str(datetime.now()))
        #self.ttlcountdown = 0

    def writeLogEntry(self, msg):
        with open(LOG_DIRECTORY+"WULog"+time.strftime("%Y%m%d")+".log", mode='a+', encoding='utf-8') as f:
            f.write(msg)

    def correctForAltitude(self, press, temp, alti):
        denom = temp + 273.15 + 0.0065 * alti
        val = (1 - (0.0065 * alti)/denom)
        press_sl = press * pow(val, -5.257)
        return press_sl

    # function using _stop function
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while True:
            if self.stopped():
                return

            self.writeLogEntry("Start Api Call: " + str(datetime.now()))
            url = BASE_URL + LIVEDATA_URL + f'stationId={self.sid}&format=json&units=m&apiKey={self.key}&numericPrecision=decimal'
            r = requests.get(url, headers=self.headers)
            if r.status_code != 200:
                # Not successful. Assume Authentication Error
                self.writeLogEntry("Request Status Error:" + str(r.status_code))
            else:
                data_dict = json.loads(r.text)['observations'][0]
                dtutc = data_dict['obsTimeUtc']
                solrad = data_dict['solarRadiation']
                windir = data_dict['winddir']
                humid = data_dict['humidity']
                uvidx = data_dict['uv']
                evt_time = datetime.strptime(dtutc, '%Y-%m-%dT%H:%M:%SZ')

                metdata = data_dict['metric']
                temp = metdata['temp']
                heatIndex = metdata['heatIndex']
                dewpt = metdata['dewpt']
                windChill = metdata['windChill']
                windSpeed = metdata['windSpeed']
                windGust = metdata['windGust']
                pressure = metdata['pressure']
                precipRate = metdata['precipRate']
                precipTotal = metdata['precipTotal']

                pressure = self.correctForAltitude(pressure, temp, 80)

                if temp > 21.1111: # 70F
                    feels_like = heatIndex
                elif temp < 16.1111: # 61
                    feels_like = windChill
                else:
                    feels_like = temp

                self.writeLogEntry(f'\n{evt_time},{temp}, {feels_like}, {pressure}, {windSpeed}, {windGust},')
                self.writeLogEntry(f'{windir}, {humid}, {uvidx}, {solrad} {dewpt}, {precipRate},{precipTotal}')

                # update openhab
                openhab = OpenHAB(getOpenhabURL())
                OutsideTemp = openhab.get_item('OutsideTemp2')
                FeelsLike = openhab.get_item('OutsideFeelsLike2')
                RelPressure = openhab.get_item('RelPressure2')

                OutsideTemp.state = temp
                FeelsLike.state = feels_like
                RelPressure.state = pressure

            time.sleep(sleep_time)
            #self.ttlcountdown -= 10


# main function
os.makedirs(LOG_DIRECTORY, exist_ok=True)
t1 = WuData(stationid, getWUkey())
t1.start()
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    t1.stop()
