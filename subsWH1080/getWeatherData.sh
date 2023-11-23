#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source /home/pi/venvs/energy/bin/activate
python $here/MQtoFile.py /home/pi/weather
