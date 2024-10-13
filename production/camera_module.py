from picamera import PiCamera
from datetime import datetime
import os

class CameraModule:
    def __init__(self, folder="photos"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)  # 创建存储文件夹（如不存在）/ Create storage folder if it doesn't exist
        self.camera = PiCamera()  # 初始化摄像头 / Initialize the camera

    def capture_photo(self):
        """拍摄照片并以时间戳命名保存到本地文件夹 / Capture a photo and save it to the local folder with a timestamp name"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        photo_path = os.path.join(self.folder, f"{timestamp}.jpg")
        self.camera.capture(photo_path)
        print(f"Photo saved: {photo_path}")

    def close(self):
        """关闭摄像头"""
        self.camera.close()
