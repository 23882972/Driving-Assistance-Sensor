import time
from datetime import datetime
from lis3dh_sensor import LIS3DH
from vl53l1x_sensor import VL53L1X
from buzzer import BUZZER
from camera_module import CameraModule
from file_logger import FileLogger
from git_handler import GitHandler
import RPi.GPIO as GPIO
import boto3
import os

# 初始化传感器 / Initialize sensors
accelerometer = LIS3DH()
distance_sensor = VL53L1X()
buzz = BUZZER()
camera = CameraModule()

# 初始化文件记录器 / Initialize file logger
file_logger = FileLogger(data_format='csv')

# 初始化 Git 处理器 / Initialize Git handler
git_handler = GitHandler()

# 初始化 S3 客户端 / Initialize S3 client
s3 = boto3.client('s3')
bucket_name = '24148088-cloudstorage'  # S3 桶名称

# 设置阈值和时间窗口参数 / Define threshold and time window parameters
ACCELERATION_THRESHOLD = 3000  # 加速度阈值 / Acceleration threshold
DISTANCE_THRESHOLD = 100  # 距离阈值 (毫米) / Distance threshold (mm)
TIME_WINDOW = 3  # 时间窗口长度 (秒) / Time window length (seconds)
MAX_ALERTS_IN_WINDOW = 3  # 时间窗口内的最大警报次数 / Max alerts in the time window
alert_times = []  # 记录警报的触发时间 / Record alert trigger times


# 上传数据到 S3 / Function to upload data to S3
def upload_to_s3(file_name, file_content, bucket_name):
    try:
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        print(f"Successfully uploaded {file_name} to S3")
    except Exception as e:
        print(f"Error uploading to S3: {e}")


# 上传照片到 S3 / Function to upload photo to S3
def upload_photo_to_s3(photo_path, bucket_name):
    try:
        with open(photo_path, "rb") as photo:
            s3.put_object(Bucket=bucket_name, Key=os.path.basename(photo_path), Body=photo)
        print(f"Photo {photo_path} uploaded successfully to S3")
    except Exception as e:
        print(f"Error uploading photo to S3: {e}")


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

        # 打印并记录数据 / Print and log data
        data_string = f"Time: {timestamp}, X: {x}, Y: {y}, Z: {z}, Total Accel: {total_accel:.2f}, Distance: {distance}\n"
        file_logger.save_data(timestamp, x, y, z, total_accel, distance)
        print(data_string)

        # 保存并上传数据到 S3 / Save and upload data to S3
        file_name = f"sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        upload_to_s3(file_name, data_string, bucket_name)

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

            # 拍摄照片并上传到 S3 / Capture photo and upload to S3
            photo_path = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            camera.capture_photo(photo_path)  # 拍摄照片 / Capture photo
            upload_photo_to_s3(photo_path, bucket_name)

            # 记录报警时间 / Record alert time
            alert_times.append(datetime.now())

            # 清理过期的报警记录 / Clean up expired alert records
            alert_times = [t for t in alert_times if (datetime.now() - t).seconds <= TIME_WINDOW]

            # 如果窗口内警报次数超过阈值，触发蜂鸣器 / Trigger buzzer if alerts exceed threshold
            if len(alert_times) >= MAX_ALERTS_IN_WINDOW:
                print("Buzzer Triggered!")
                buzz.buzz_three_times()  # 蜂鸣器鸣叫三次 / Buzzer buzzes three times

        # 每隔 10 秒执行 Git 提交和推送 / Commit and push to Git every 10 seconds
        git_handler.commit_and_push()

        # 等待下一次循环 / Wait for next iteration
        time.sleep(5)  # 数据每 5 秒上传一次 / Data uploads every 5 seconds

finally:
    buzz.buzzer_off()  # 关闭蜂鸣器 / Turn off the buzzer
    GPIO.cleanup()  # 清理 GPIO 引脚设置 / Clean up GPIO pin settings
