#!/bin/bash

# copyright Mark McIntyre, 2023-

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here

weatherdir=/home/pi/weather

source /home/pi/venvs/pywws/bin/activate
rm -f $weatherdir/stopbmp280
python $here/readBmp280.py $weatherdir
