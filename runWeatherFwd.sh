#!/bin/bash
source ~/venvs/openhabstuff/bin/activate
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
cd ~/source/openhabstuff/weatherfwd
python weatherFwd.py
