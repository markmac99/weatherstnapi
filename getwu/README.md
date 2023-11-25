# README for getwu

My Bresser 5-in-1 weatherstation has very limited interfaces to collect data from it programatically.
However, you can configure the station to publish to Weather Underground.

## Indoor sensors
This programme collects the *indoor* sensors data from Weather Underground via their API and publishes it to MQTT. These data are not otherwise published by the unit.

## Outdoor sensors
You can also intercept the data via *rtl_433*, which can read the *outdoor* sensors and publish 
their values to MQTT. So i have *rtl_433* running on a Pi to publish the external data, and 
this programme listening to Weather Underground to read back the other data and publish it. 

## Openhab
The programme also publishes some data to my OpenHAB installation, via OpenHAB's cloud API gateway. 

## Keys
To use Weather Underground you'll need a StationID and API Key. 
To use Openhab you'll need an OH username and password. 
* The WU stationID should be updated in *wuconfig.py*
* The WU API key must be stored in *~/.ssh/wupass*. This file should be set to 0600 permissions and consdered secret.
* The OH user/pass must be stored in *~/.ssh/myohpass* on separate lines. Again treat this as a secret file. 
