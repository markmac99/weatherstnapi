#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source /home/ec2-user/venvs/openhabstuff/bin/activate
python getwu.py
