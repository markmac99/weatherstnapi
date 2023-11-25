# weatherstnapi
Various small services and APIs to handle weatherstation data

* getwu - read data from WeatherUnderground and republish it on MQTT
* readBmp280 - read pressure,temperature and humidity data from a BMP280/BME280 breakout board and publish it to MQTT
* rtl433ToMQ - read data from rtl-sdr ompatible 433/838MHz outdoor weather sensors and publish on MQTT
* subWH1080 - subscribe to MQTT and write data to a file suitable for ingestion by pywws

Legacy functions
* weatherapi - flask app to publish WH1080 data via an API. Used before MQ was built into pywws
* weatherfwd - took data from the above API and posted it to my openhab server. 
