import requests
import json
import threading
import time
from openhab import OpenHAB


openhab_URL ='http://wxsatpi:8080/rest'


class WeatherFwd(threading.Thread):

    # Thread class with a _stop() method.
    # The thread itself has to check
    # regularly for the stopped() condition.

    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        openhab = OpenHAB(openhab_URL)
        self.OutsideTemp = openhab.get_item('OutsideTemp')
        self.InsideTemp = openhab.get_item('HouseTemperature')

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
                res = requests.get('http://weatherpi:5000/values')
                data = json.loads(res.text)[0]
                tempin = float(data['temp_in'])
                res2 = requests.get('http://weatherpi:5000/tempout')
                data2 = json.loads(res2.text)[0]
                #print(data2)
                tempout = float(data2['temp_out'])
                print(tempin, tempout)
                self.OutsideTemp.state = tempout
                self.InsideTemp.state = tempin
            except:
                pass
            time.sleep(187)


t1 = WeatherFwd()
t1.start()
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    t1.stop()
