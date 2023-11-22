#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source /home/pi/venvs/pywws/bin/activate
rm -f $here/stopwhfwd
python $here/rtl43ToMQ.py $here/maplinstn/weatherdata.json
