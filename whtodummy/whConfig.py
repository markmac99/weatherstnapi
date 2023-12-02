# 
# copyright 2023 mark mcintyre
# 
# edit this file to reflect the location of the files created by rtl_433 and readbmp280
# and the location of the file that will be read by the dummy USB driver for pywws

def loadConfig():
    whfile = '/home/pi/weather/maplinstn/weatherdata.json'
    bpfile = '/home/pi/weather/maplinstn/bmp280.json'
    targfile = '/home/pi/weather/weatherdata.json'        
    return whfile, bpfile, targfile
