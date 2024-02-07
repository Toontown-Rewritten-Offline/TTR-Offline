#!/usr/bin/env sudo /Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9
cd ../../
MAX_CHANNELS=999999
STATE_SERVER=4002
ASTRON_IP="127.0.0.1:7199"
EVENT_LOGGER_IP="127.0.0.1:7197"
BASE_CHANNEL=1000000

python3 -m toontown.uberdog.ServiceStartUD --base-channel $BASE_CHANNEL \
               --max-channels $MAX_CHANNELS --stateserver $STATE_SERVER \
               --astron-ip $ASTRON_IP --eventlogger-ip $EVENT_LOGGER_IP