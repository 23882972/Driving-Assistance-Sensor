import time
import csv
import RPi.GPIO as GPIO
from datetime import datetime
from lis3dh_sensor import LIS3DH
from vl53l1x_sensor import VL53L1X

# 初始化传感器
accelerometer = LIS3DH()
distance_sensor = VL53L1X()

# 配置蜂鸣器引脚
BUZZER_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# 定义阈值
ACCELERATION_THRESHOLD = 3000  # 假设加速度阈值，单位与 LIS3DH 读取的数值一致
DISTANCE_THRESHOLD = 100  # 假设距离阈值，单位为毫米


# 保存数据到 CSV 文件并写入表头
def initialize_csv_file():
    with open("sensor_data.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "X_Axis", "Y_Axis", "Z_Axis", "Total_Acceleration", "Distance"])


def initialize_alert_log():
    with open("alert_log.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Alert_Reason"])


def save_data_to_csv(timestamp, x, y, z, total_accel, distance):
    with open("sensor_data.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, x, y, z, total_accel, distance])


def save_alert_log(timestamp, reason):
    with open("alert_log.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, reason])


# 蜂鸣器警报
def trigger_buzzer(duration=1):
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(BUZZER_PIN, GPIO.LOW)


# 初始化 CSV 文件，确保文件包含表头
initialize_csv_file()
initialize_alert_log()

# 设置数据保存间隔
save_interval = 5  # 每 5 秒保存一次数据
last_saved_time = 0

# 主循环，读取数据并保存
try:
    while True:
        # 读取加速度传感器数据
        x, y, z = accelerometer.read_acceleration()
        total_accel = accelerometer.calculate_total_acceleration(x, y, z)

        # 读取距离传感器数据
        distance = distance_sensor.read_distance()

        # 获取当前时间
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 打印读取数据到控制台
        print(f"Time: {timestamp}, X: {x}, Y: {y}, Z: {z}, Total Accel: {total_accel:.2f}, Distance: {distance}")

        # 检查阈值并触发警报
        alert_triggered = False
        code = -1
        alert_reason = ""

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
            save_alert_log(timestamp,code, alert_reason)
            trigger_buzzer(1)  # 启动蜂鸣器 1 秒

        # 保存数据到 CSV 文件
        current_time = time.time()
        if current_time - last_saved_time > save_interval:
            save_data_to_csv(timestamp, x, y, z, total_accel, distance)
            last_saved_time = current_time  # 更新最后保存时间

        # 等待下一次循环
        time.sleep(1)

finally:
    GPIO.cleanup()  # 清理 GPIO 引脚设置
