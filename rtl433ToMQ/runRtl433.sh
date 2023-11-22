#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
/usr/local/bin/rtl_433 -R 32 -R 155 -F json::/home/pi/weather/maplinstn/weatherdata.json
