import math
import smbus2 as smbus

# Class for calculation of the total acceleration
class LIS3DH:
    def calculate_total_acceleration(self, x, y, z):
        return math.sqrt(x**2 + y**2 + z**2)
