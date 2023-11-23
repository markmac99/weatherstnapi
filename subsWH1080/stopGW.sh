#!/bin/bash
here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
pid=$(ps -ef | grep MQtoFile | grep -v grep | awk '{print $2}')
kill -9 $pid
