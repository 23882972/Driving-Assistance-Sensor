import subprocess
import time

while True:
    time.sleep(20)
    subprocess.run(["/home/csseiot/final/Driving-Assistance-Sensor/updatecsv.sh"])
    

