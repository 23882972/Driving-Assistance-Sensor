import smbus2
import time

class VL53L1X:
    def __init__(self, bus_num=1, address=0x29):
        self.bus = smbus2.SMBus(bus_num)
        self.address = address
        self.initialize_sensor()

    def initialize_sensor(self):
        # 初始化命令序列：设定 VL53L1X 的默认配置 / Initialization command sequence: Set the default configuration of VL53L1X
        self.bus.write_byte_data(self.address, 0x00, 0x01)  # 示例：写入启动命令
        time.sleep(0.1)
	
    def read_distance(self):
        # 读取距离数据 / Read distance data
        # 获取2个字节的数据 / Get 2 bytes of data
        try:
            data = self.bus.read_i2c_block_data(self.address, 0x00, 2)  # 根据 VL53L1X 数据手册设置寄存器地址
            distance = (data[0] << 8) | data[1]  # 将高字节和低字节组合成完整的距离数据
            return distance
        except IOError:
            print("Failed to read from sensor")
            return None
