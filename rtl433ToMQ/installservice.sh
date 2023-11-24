#!/bin/bash

# copyright Mark McIntyre, 2023-

# install service to read from my WH1080 / Maplin weatherstation outdoor sensors

# pretty sure this needs apt-get install rtl-sdr librtlsdr-dev
# rtl_433 should be downloaded from github and built locally

# rtl_433 should be able to publish to MQ but I'm having problems with it. 
# might work on a new build pi

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

sudo cp rtl2mq.service /etc/systemd/system/
sudo cp rtl_433.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rtl2mq
sudo systemctl start rtl2mq
sudo systemctl enable rtl_433
sudo systemctl start rtl_433
