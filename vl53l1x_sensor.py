import board
import busio
import adafruit_vl53l1x

class VL53L1X:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l1x.VL53L1X(i2c)
        self.sensor.distance_mode = 2
        self.sensor.timing_budget = 100

    def read_distance(self):
        if self.sensor.data_ready:
            return self.sensor.distance
        else:
            return None
