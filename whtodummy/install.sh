#!/bin/bash

# copyright Mark McIntyre, 2023-

# install cronjob to copy data for pywws

here="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $here
appname=whTodummy.sh

if [ "$(crontab -l | grep $appname)" == "" ] ; then 
    echo "installing cron job"
    (crontab -l && echo "* * * * * $here/$appname > /dev/null 2>&1" ) | crontab -
else
    echo "nothing to install"
fi
