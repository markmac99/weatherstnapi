#!/bin/bash
source ~/venvs/pywws/bin/activate
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
export FLASK_APP=$here/weatherapi.py
export DATAFILE=$HOME/weather/weatherdata.json

python -m flask run --host=0.0.0.0 -p 8081
