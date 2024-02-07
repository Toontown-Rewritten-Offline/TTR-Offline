#!/bin/bash

# Change to the desired directory
cd ../../astron

# Check if the process is running
if pgrep -x "astrondmac" > /dev/null
then
    # If the process is running, gracefully terminate it
    sudo pkill -x "astrondmac"
fi

# Run the command
sudo ./astrondmac --loglevel info config/astrond-yaml.yml