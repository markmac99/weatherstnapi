#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
pid=$(ps -ef |egrep " python -m flask run --host=0.0.0.0 -p 8081" | grep -v grep | awk '{print $2}')
/bin/kill $pid
