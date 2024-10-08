import math
import smbus


# Accelerometer LIS3DH sensor

class LIS3DH:
    def __init__(self, address=0x2b, bus_num=1):
        self.address = address
        self.bus = smbus.SMBus(bus_num)
        self.initialize_sensor()

    def initialize_sensor(self):
        self.bus.write_byte_data(self.address, 0x20, 0x27)
        self.bus.write_byte_data(self.address, 0x23, 0x00)

    def read_acceleration(self):
        x = self.bus.read_byte_data(self.address, 0x28) | (self.bus.read_byte_data(self.address, 0x29) << 8)
        y = self.bus.read_byte_data(self.address, 0x2A) | (self.bus.read_byte_data(self.address, 0x2B) << 8)
        z = self.bus.read_byte_data(self.address, 0x2C) | (self.bus.read_byte_data(self.address, 0x2D) << 8)

        if x > 32767: x -= 65536
        if y > 32767: y -= 65536
        if z > 32767: z -= 65536

        x_offset, y_offset, z_offset = 0, 0, 16384  # 示例值，根据量程调整
        x = x - x_offset
        y = y - y_offset
        z = z - z_offset
        return x, y, z

    def calculate_total_acceleration(self, x, y, z):
        return math.sqrt(x**2 + y**2 + z**2)