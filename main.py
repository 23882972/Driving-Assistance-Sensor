import time
from datetime import datetime
from lis3dh_sensor import LIS3DH
from vl53l1x_sensor import VL53L1X
from buzzer import BUZZER
from camera_module import CameraModule
from file_logger import FileLogger
import RPi.GPIO as GPIO
import subprocess
from PiicoDev_LIS3DH import PiicoDev_LIS3DH
from PiicoDev_VL53L1X import PiicoDev_VL53L1X

# Initializing instances
motion = PiicoDev_LIS3DH() # Instance to read the accelerometer
motion.range = 2
accelerometer = LIS3DH() # Instance to calculate the total acceleration
distance_sensor = PiicoDev_VL53L1X() # Instance to read the distance sensor
buzz = BUZZER() # Instance for buzzer
camera = CameraModule() # Instance for camera

# Defining thresholds and time window parameters
ACCELERATION_THRESHOLD = 10
DISTANCE_THRESHOLD = 200
TIME_WINDOW = 3
MAX_ALERTS_IN_WINDOW = 3

# Initializing file logger
file_logger = FileLogger(data_format='csv')
        
# Setting parameters
save_interval = 5  # Saving data every 5 seconds
last_saved_time = 0
alert_times = []  # Recording the time when alerts were triggered


# Main loop to read and save the data
try:
    while True:
        # Reading accelerometer data
        x, y, z = motion.acceleration
	
	# Calculating total acceleration
        total_accel = accelerometer.calculate_total_acceleration(x, y, z)

        # Reading distance sensor data
        distance = distance_sensor.read()

        # Getting current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Printing data to console and saving it into the CSV file
        file_logger.save_data(timestamp, x, y, z, total_accel, distance, 'false')
        print(f"Time: {timestamp}, X: {x}, Y: {y}, Z: {z}, "
              f"Total Accel: {total_accel:.2f}, Distance: {distance}")

        # Checking thresholds and recording alerts
        alert_triggered = False
        code, alert_reason = -1, ""

        if total_accel > ACCELERATION_THRESHOLD:
            alert_triggered = True
            code = 0
            alert_reason = "Acceleration Threshold Exceeded"
        elif distance is not None and distance < DISTANCE_THRESHOLD:
            alert_triggered = True
            code = 1
            alert_reason = "Distance Below Threshold"

        if alert_triggered:
            print(f"Alert: {alert_reason}")
            file_logger.save_alert_log(timestamp, code, alert_reason) # Saving the data if alert is triggered
            camera.capture_photo()  # Capturing photo if alert is triggered
            alert_times.append(datetime.now())

            # Cleaning up expired alert records
            alert_times = [t for t in alert_times if (datetime.now() - t).seconds <= TIME_WINDOW]

            # Triggering the buzzer if alert count exceeds threshold in window
            if len(alert_times) >= MAX_ALERTS_IN_WINDOW:
                print("Buzzer Triggered!")
                buzz.buzz_three_times()  # Buzzering 3 times

        # Pause before the next iteration
        time.sleep(0.5)
        

finally:
    buzz.buzzer_off()  # Turning off the buzzer
    GPIO.cleanup()  # Cleaning up GPIO


