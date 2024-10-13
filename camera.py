import picamera2
import time

camera = picamera2.Picamera2()
camera.start()
time.sleep(2)
camera.capture_file('pic.jpg')
camera.stop()
