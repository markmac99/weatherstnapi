import json
import os


def getData(fname):
    reslist = None
    try:
        reslist = json.load(open(fname))
    except Exception:
        pass
    return reslist


def getOutsideTemp(fname):
    reslist = getData(fname)
    return reslist['temperature_C']


if __name__ == '__main__':
    fname = os.getenv('DATAFILE', default='/home/pi/weather/weatherdata.json')
    res = getData(fname)
    print(res['temperature_C'])
