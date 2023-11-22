#!/bin/bash

# copyright Mark McIntyre, 2023-

# install WU service to read from my bresser

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

sudo cp bmp280.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable bmp280
sudo systemctl start bmp280
