# subWH1010

This programme subscribes to data from my WH1080 weatherstation being published via MQ, and
to data being captured from a BME280 sensor chip. The data are written to a file which i am consuming with a dummy USB driver for pywws.

The reason behind this is that my Weatherstation's USB port is defective so i can no longer read data over USB. However, the outdoor sensors still work fine, and so i am capturing the data from those via an RTL-SDR dongle (see elsewhere in this repo) and publishing to MQ. This allows me to use the data in OpenHAB, however i also want to keep
running pywws, the weatherstation software. This expects data via USB so I've written a dummy USB driver that reads the file created by this programme and presents it to pywws as if it were read from the USB port. 

As the external sensors don't include indoor pressure, temperature and humidity, I also connected a BME280 sensor to my Pi and am collecting data from it too. This is also published via MQ and then read back again and included in the data file.
