import RPi.GPIO as GPIO
import time

class BUZZER:
    def __init__(self, pin=18):
        self.pin = pin
        self.init_buzzer()

    def init_buzzer(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def buzzer_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def buzzer_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def buzz_three_times(self):
        for _ in range(3):
            self.buzzer_on()
            time.sleep(0.2)
            self.buzzer_off()
            time.sleep(0.1)

    def cleanup(self):
        GPIO.cleanup()