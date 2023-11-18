#!/bin/bash
#source ~/venvs/energy/bin/activate
export FLASK_APP=weatherapi.py
cd ~/source/weatherapi
python -m flask run --host=0.0.0.0
