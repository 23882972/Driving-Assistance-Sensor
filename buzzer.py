import RPi.GPIO as GPIO
import time

# Creating a class to control the buzzer
class BUZZER:
    # Initializing buzzer object
    def __init__(self, pin=18):
        self.pin = pin
        self.init_buzzer()
    # Setting up the GPIO pin for output
    def init_buzzer(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
    # Turning the buzzer on
    def buzzer_on(self):
        GPIO.output(self.pin, GPIO.HIGH)
    # Turning the buzzer off
    def buzzer_off(self):
        GPIO.output(self.pin, GPIO.LOW)
    # Setting a buzzer for alert 3 times with pauses in between
    def buzz_three_times(self):
        for _ in range(3):
            self.buzzer_on()
            time.sleep(0.2)
            self.buzzer_off()
            time.sleep(0.1)
    # Cleaning up
    def cleanup(self):
        GPIO.cleanup()
