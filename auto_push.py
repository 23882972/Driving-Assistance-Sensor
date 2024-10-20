import subprocess
import time
# While loop to run the update.sh script every 20 seconds
while True:
    time.sleep(20)
    subprocess.run(["/home/csseiot/final/updatecsv.sh"])
