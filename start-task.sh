#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Usage: ./start-task.sh USERID"
    exit -1
fi

## Clear up any previous leftover logs
rm -f /vagrant/timeline.log

## Start browser monitoring process
if pgrep -x "mitmdump" > /dev/null
then
    echo "Monitoring already running? Maybe an ERROR."
else
    echo "Starting monitoring"
    ## Clear up any previous leftover logs
    rm -f /vagrant/browser_requests.log
    /usr/local/bin/mitmdump -q --set stream_large_bodies=1 -s /vagrant/browser-request-logger.py &
fi

## Retrieve task and configure & start pycharm
python3 retrieve_assignments.py assign $1

## log
TIMESTAMP=`date +"%s"`
echo -e "${TIMESTAMP}\tTask started" >> /vagrant/timeline.log