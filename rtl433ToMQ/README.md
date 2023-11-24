# README for rtl433ToMQ

This code reads from a WH1080 / Maplin weatherstation and posts the results to MQTT

The process makes use of rtl_433, which can natively write to MQ however, i found that 
this would not work on my Pi. Additionally i wanted to post some derived data not available 
directly from the weatherstation such as dew point, wind chill and heat index. 

## Prerequisites
You'll need to install rtl-sdr and its development libraries, plus development tools to build rtl_433. I 
also strongly recommend you install into a python virtual environment.
``` bash
sudo apt-get install rtl-sdr librtlsdr-dev
sudo apt-get install libtool libusb-1.0-0-dev librtlsdr-dev rtl-sdr build-essential cmake pkg-config
sudo apt-get install python3-venv
```
## Building rtl_433
Download the code from github, then build and install it:
``` bash
mkdir source 
cd source
git clone https://github.com/merbanan/rtl_433.git
cd rtl_433
mkdir build
cd build
cmake ..
make
sudo make install
```

## Testing rtl_433, and a possible gotcha
Test rtl_433 by plugging in your RTL-SDR dongle, and running 
```bash
rtl_433
```
If you get an error that permissions are wrong, copy the UDEV rules file and restart the pi
``` bash
sudo cp rtl-sdr.rules /etc/udev/rules.d
sudo reboot
```
rtl-sdr.rules is in this git repository.  
You should now be able to run rtl_sdr without error.

# Install rtl_433 and rtl2mq 
Make a folder in the pi user's home directory called *~/weather* and copy all files from this repo into this location. Now create a python virtual environment, activate it and install the python libraries. 
``` bash
mkdir -p ~/weather
cp *.sh *.py *.service  ~/weather
mkdir -p ~/venvs
python3 -m venv ~/venvs/pywws
source ~/venvs/pywws/bin/activate
pip install -r ~/weather/requirements.txt
```

Edit the config file *mqConfig.py* to reference your MQTT broker and port, then you can install and start the services.  

``` bash
cd ~/weather
./installservice.sh
```
This should install two services *rtl_433* which reads from the weatherstation sensors, and *rtl2mq* which 
forwards data to MQTT.  Test that both services are running as follows: 
```bash
systemctl status rtl_433
systemctl status rtl2mq
```

*rtl_433* writes data to a file *~/weather/maplinstn/weatherdata.json* which you may need to periodically delete
to save space. The system will recreate it automatically. 

The service logfiles are written to *~/weather/logs*, and messages may also be logged to syslog. 