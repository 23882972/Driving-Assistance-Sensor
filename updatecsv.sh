#!/bin/bash

. /home/csseiot/.bashrc

cd /home/csseiot/final/Driving-Assistance-Sensor

git add /home/csseiot/final/Driving-Assistance-Sensor/sensor_data.csv /home/csseiot/final/Driving-Assistance-Sensor/photos/ /home/csseiot/final/Driving-Assistance-Sensor/alert_log.csv

git commit -m "Auto-push: $(date '+%Y-%m-%d %H:%M:%S')"

git push https://$MYTOKEN@github.com/23882972/Driving-Assistance-Sensor.git
