#!/bin/bash

cd ~/Desktop/iot/Driving-Assistance-Sensor

git add ~/Desktop/iot/Driving-Assistance-Sensor/sensor_data.csv

git commit -m "Auto-push: $(date '+%Y-%m-%d %H:%M:%S')"

csvgitpush
