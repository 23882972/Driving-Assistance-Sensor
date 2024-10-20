from picamera2 import Picamera2
from datetime import datetime
import os

# Class for the camera usage
class CameraModule:
    # Initializing an object
    def __init__(self, folder="/home/csseiot/final/Driving-Assistance-Sensor/photos"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)  # Creating storage folder if it doesn't exist
        self.camera = Picamera2()  # Initializing the camera
        self.camera.start()

    # Capturing a photo and saving it to the local folder with a timestamp name"
    def capture_photo(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        photo_path = os.path.join(self.folder, f"{timestamp}.jpg")
        self.camera.capture_file(photo_path)
        print(f"Photo saved: {photo_path}")

    # Switching off
    def close(self):
        self.camera.stop()
