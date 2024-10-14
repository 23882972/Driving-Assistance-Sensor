import time
from datetime import datetime
from lis3dh_sensor import LIS3DH
from vl53l1x_sensor import VL53L1X
from buzzer import BUZZER
from camera_module import CameraModule
from file_logger import FileLogger
from git_handler import GitHandler  # 导入 GitHandler 类
import RPi.GPIO as GPIO

# 初始化传感器 / Initialize sensors
accelerometer = LIS3DH()
distance_sensor = VL53L1X()
buzz = BUZZER()
camera = CameraModule()

# 定义阈值和时间窗口参数 / Define threshold and time window parameters
ACCELERATION_THRESHOLD = 3000  # 加速度阈值/ Acceleration threshold
DISTANCE_THRESHOLD = 100  # 距离阈值 (毫米)/ Distance threshold (mm)
TIME_WINDOW = 3  # 时间窗口长度 (秒) / Time window length (seconds)
MAX_ALERTS_IN_WINDOW = 3  # 时间窗口内的最大报警次数 / Maximum number of alerts in the time window

# 初始化文件记录器 / Initialize file logger
file_logger = FileLogger(data_format='csv')

# 初始化 Git 处理器 / Initialize Git handler
git_handler = GitHandler()
        
# 设置参数 / Set parameters
save_interval = 5  # 每 5 秒保存一次数据 / Save data every 5 seconds
last_saved_time = 0
alert_times = []  # 记录触发警报的时间 / Record the time when alerts were triggered

# 主循环，读取数据并保存 / Main loop to read data and save
try:
    while True:
        # 读取加速度数据 / Read accelerometer data
        x, y, z = accelerometer.read_acceleration()
        total_accel = accelerometer.calculate_total_acceleration(x, y, z)

        # 读取距离传感器数据 / Read distance sensor data
        distance = distance_sensor.read_distance()

        # 获取当前时间 / Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 打印数据到控制台 / Print data to console
        file_logger.save_data(timestamp, x, y, z, total_accel, distance)
        print(f"Time: {timestamp}, X: {x}, Y: {y}, Z: {z}, "
              f"Total Accel: {total_accel:.2f}, Distance: {distance}")

        # 检查阈值并记录警报 / Check thresholds and record alerts
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
            file_logger.save_alert_log(timestamp, code, alert_reason)
            camera.capture_photo()  # 拍摄照片
            alert_times.append(datetime.now())

            # 清理过期的报警记录 / Clean up expired alert records
            alert_times = [t for t in alert_times if (datetime.now() - t).seconds <= TIME_WINDOW]

            # 如果窗口内报警次数超过阈值，触发蜂鸣器 / Trigger buzzer if alert count exceeds threshold in window
            if len(alert_times) >= MAX_ALERTS_IN_WINDOW:
                print("Buzzer Triggered!")
                buzz.buzz_three_times()  # 蜂鸣器鸣叫三次 / Buzzer buzzes three times


        # 每隔 10 秒执行 Git 提交和推送 / Commit and push to Git every 10 seconds
        git_handler.commit_and_push()

        # 等待下一次循环 / Wait for next iteration
        time.sleep(0.5)

finally:
    buzz.buzzer_off()  # 关闭蜂鸣器 / Turn off the buzzer
    GPIO.cleanup()  # 清理 GPIO 引脚设置 / Clean up GPIO pin settings