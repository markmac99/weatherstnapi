#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
source $HOME/venvs/openhabstuff/bin/activate
python $here/MQtoFile.py $here
