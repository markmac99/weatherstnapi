#!/bin/bash

# copyright Mark McIntyre, 2023-

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source /home/pi/venvs/breakouts/bin/activate
rm -f $here/stopbmp280
mkdir -p $here/logs
python $here/readBmp280.py
