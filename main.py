import csv
import time
from datetime import datetime
from lis3dh_sensor import LIS3DH
from vl53l1x_sensor import VL53L1X

# 初始化传感器
accelerometer = LIS3DH()
distance_sensor = VL53L1X()

# Initialize CSV file with header row
def initialize_csv():
    with open("acceleration_data.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "X_Axis", "Y_Axis", "Z_Axis", "Total_Acceleration"])


def save_data_to_file(timestamp, x, y, z, total_accel, distance):
    with open("sensor_data.txt", "a") as file:
        file.write(f"{timestamp}, X: {x}, Y: {y}, Z: {z}, Total Accel: {total_accel}, Distance: {distance}\n")


save_interval = 5  # 保存数据的间隔时间（秒）
last_saved_time = 0

initialize_csv()  # Initialize CSV file

while True:
    # 读取加速度传感器的数据
    x, y, z = accelerometer.read_acceleration()
    total_accel = accelerometer.calculate_total_acceleration(x, y, z)

    # 读取距离传感器的数据
    distance = distance_sensor.read_distance()

    # 获取当前时间
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 打印读取数据
    print(f"Time: {timestamp}, X: {x}, Y: {y}, Z: {z}, Total Accel: {total_accel:.2f}, Distance: {distance}")

    # 保存数据到文件
    current_time = time.time()
    if current_time - last_saved_time > save_interval:
        save_data_to_file(timestamp, x, y, z, total_accel, distance)
        last_saved_time = current_time  # 更新最后保存时间

    time.sleep(1)  # 设置循环时间间隔
