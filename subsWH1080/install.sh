#!/bin/bash

# copyright Mark McIntyre, 2023-

# install WU service to read from my bresser

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

sudo cp getweather.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable getweather
sudo systemctl start getweather
