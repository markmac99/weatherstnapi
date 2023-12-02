#!/bin/bash

# copyright Mark McIntyre, 2023-

# install service to read from my WH1080 / Maplin weatherstation outdoor sensors
# and republish on MQ, with some additional derived data

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

sudo cp rtl2mq.service /etc/systemd/system/
sudo cp rtl_433.service /etc/systemd/system/
sudo cp rtl-sdr.rules /etc/udev/rules.d/
sudo systemctl daemon-reload
echo need to reboot now
sudo systemctl enable rtl2mq
sudo systemctl start rtl2mq
sudo systemctl enable rtl_433
sudo systemctl start rtl_433
