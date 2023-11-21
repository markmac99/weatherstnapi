#!/bin/bash

# copyright Mark McIntyre, 2023-

# install WU service to read from my bresser

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

sudo cp rtl2mq.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rtl2mq
sudo systemctl start rtl2mq
