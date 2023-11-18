import requests
import json
import threading
import time
from openhab import OpenHAB

# ATTENTION: don't use f-strings to maintain Python 3.5 compatability


openhab_URL = 'http://wxsatpi:8080/rest'
weather_URL = 'http://weatherpi:5000'

class WeatherFwd(threading.Thread):

    # Thread class with a _stop() method.
    # The thread itself has to check
    # regularly for the stopped() condition.

    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

    # function using _stop function
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        while True:
            if self.stopped():
                return
            try: 
                openhab = OpenHAB(openhab_URL)
                OutsideTemp = openhab.get_item('OutsideTemp')
                InsideTemp = openhab.get_item('HouseTemperature')
                FeelsLike = openhab.get_item('OutsideFeels')
                RelPressure = openhab.get_item('RelPressure')
                Humidity = openhab.get_item('Humidity_m')
                RainRate = openhab.get_item('RainRate_m')
                WindSpeed = openhab.get_item('WindSpeed_m')
                WindGust = openhab.get_item('WindGust_m')
                WindDir = openhab.get_item('WindDir_m')
            except:
                print('problem connecting to openhab')
            else:
                res = requests.get(weather_URL+'/values', timeout=10)
                if res.status_code == 200:
                    data = json.loads(res.text)[0]
                    tempin = float(data['temp_in'])
                    feels = float(data['feels_like'])
                    press = float(data['rel_pressure'])
                    hum = float(data['hum_out'])
                    rain = float(data['rain'])
                    wind_s = float(data['wind_ave'])
                    wind_g = float(data['wind_gust'])
                    wind_d = float(data['wind_dir'])
                    try:
                        InsideTemp.state = tempin
                        FeelsLike.state = feels
                        RelPressure.state = press
                        Humidity.state = hum
                        RainRate.state = rain
                        WindSpeed.state = wind_s
                        WindGust.state = wind_g
                        WindDir.state = wind_d
                    except: 
                        print('unable to update openhab')
                    print(tempin, feels, press)
                else:
                    print('unable to reach weatherstation')

                res2 = requests.get(weather_URL+'/tempout', timeout=10)
                if res2.status_code == 200:
                    data2 = json.loads(res2.text)[0]
                    tempout = float(data2['temp_out'])
                    try:
                        OutsideTemp.state = tempout
                    except: 
                        print('unable to update openhab with tempout')
                    print(tempout)
                else:
                    print('unable to reach weatherstation')          

            time.sleep(187)


t1 = WeatherFwd()
t1.start()
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    t1.stop()
