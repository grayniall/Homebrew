#!/bin/bash

sudo apt-get update
apt-get install python-requests

echo "installing sensor into config.txt"
sh -c "echo 'dtoverlay=w1-gpio' >> /boot/config.txt"

echo "Initialising probes"
modprobe w1-gpio
modprobe w1-therm

cd /sys/bus/w1/devices
echo "You should see 28- folders below"

ls