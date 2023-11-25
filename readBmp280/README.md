# README for readBmp280

This programme reads pressure, temperature and humidity from a BMP280/bME280 sensor attached to a Pi.

## Connection to the Pi
``` bash
Vin => 1 (or any 3.3v pin) 
Sda => 3 (but can be any of GP02,06,10,14,18,26)
Scl => 5 (but can be any of GP03,07,11,15,19,27)
Gnd => 9 (or any Gnd pin)
```

## Python Requirements
I recommend creating a python virtual environment. Mine is called pywws: if you choose a different name you'll need to updte *bmp280.sh* to activate it properly. 
Requirements are *paho-mqtt*, *smbus* and *bme280* and can be installed with pip using the requirements file. 

## Configuration
Insert your MQ broker and port details into *mqConfig.py*
Also in this file, set your station's altitude above sea level. This is used to calibrate the pressure. 

## Installation
Run the *installservice.sh* script. This will install and start a service *bmp280*

# Output
The programme generates a log in *./logs*
The programme generates a JSON file in *./maplinstn* containing the most recent data. 
You'll need to periodically delete this file to save space. 

# MQ output
The service publishes to four MQTT topics 
* bmp280/temp_in_c
* bmp280/press_rel
* bmp280/humidity_in
* bmp280/time 

The last is the timestamp of the data, so you can check for stale values. 
